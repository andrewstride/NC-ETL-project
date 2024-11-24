from src.week2_lambda import lambda_handler
from testfixtures import LogCapture
from moto import mock_aws
import pytest


@pytest.fixture(scope="function")
def test_event_input():
    csv_files_written = {
        "staff": "staff/staff_2024-11-18 19_15_01.821957.csv",
        "design": "design/design_2024-11-18 19_15_01.821957.csv",
    }
    timestamps_written = ["design_timestamp.json", "staff_timestamp.json"]
    return {
        "response": 200,
        "csv_files_written": csv_files_written,
        "timestamp_json_files_written": timestamps_written,
    }


# class TestLambda2:
#     @mock_aws
#     def test_returns_dict(self, test_event_input):
#         assert isinstance(lambda_handler(test_event_input, {}), dict)

#     @mock_aws
#     def test_returns_parquet_files_written_in_dict(self, test_event_input):
#         output = lambda_handler(test_event_input, {})
#         assert list(output["parquet_files_written"].keys()) == [
#             "dim_staff",
#             "dim_design",
#         ]
