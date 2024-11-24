from src.week2_lambda import lambda_handler
from testfixtures import LogCapture
from moto import mock_aws
from unittest.mock import patch
import pytest


@pytest.fixture(scope="function")
def test_event_input():
    csv_files_written = {
        "staff": "staff/staff_2022-11-03 14_20_51.563000.csv",
        "design": "design/design_2024-11-18 19_15_01.821957.csv",
    }
    timestamps_written = ["design_timestamp.json", "staff_timestamp.json"]
    return {
        "response": 200,
        "csv_files_written": csv_files_written,
        "timestamp_json_files_written": timestamps_written,
    }


class TestLambda2:
    @mock_aws
    def test_returns_dict(self, test_event_input):
        assert isinstance(lambda_handler(test_event_input, {}), dict)

    @patch("src.week2_lambda.boto3")
    def test_returns_parquet_files_written_in_dict(
        self, mock_boto3, ingestion_bucket, test_event_input
    ):
        # patch in s3 connection with filled ingestion bucket and empty processing bucket
        mock_boto3.client.return_value = ingestion_bucket
        # Run function
        output = lambda_handler(test_event_input, {})
        # Collect output info and bucket contents
        pq_written = output["parquet_files_written"]
        response = ingestion_bucket.list_objects(Bucket="nc-terraformers-processing")
        content_list = [item["Key"] for item in response["Contents"]]
        # Assert output contains corresponding written file info that matches bucket contents
        for filepath in list(pq_written.values()):
            assert filepath in content_list
        assert list(pq_written.keys()) == [
            "dim_staff",
            "dim_design",
        ]
