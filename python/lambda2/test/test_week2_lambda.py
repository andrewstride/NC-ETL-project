from src.week2_lambda import lambda_handler
from testfixtures import LogCapture
from moto import mock_aws
from unittest.mock import patch
from io import BytesIO
import pytest
import pandas as pd


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


@pytest.fixture(scope="function")
def test_event_input_sales_order():
    csv_files_written = {
        "sales_order": "sales_order/sales_order_2024-11-20 16_18_09.992000.csv",
    }
    timestamps_written = ["sales_order_timestamp.json"]
    return {
        "response": 200,
        "csv_files_written": csv_files_written,
        "timestamp_json_files_written": timestamps_written,
    }


@pytest.fixture(scope="function")
def test_event_address():
    csv_files_written = {
        "address": "address/address_2022-11-03 14_20_49.962000.csv",
    }
    timestamps_written = ["address_timestamp.json"]
    return {
        "response": 200,
        "csv_files_written": csv_files_written,
        "timestamp_json_files_written": timestamps_written,
    }


@pytest.fixture(scope="function")
def test_event_currency():
    csv_files_written = {
        "currency": "currency/currency_2022-11-03 14_20_49.962000.csv",
    }
    timestamps_written = ["currency_timestamp.json"]
    return {
        "response": 200,
        "csv_files_written": csv_files_written,
        "timestamp_json_files_written": timestamps_written,
    }


@pytest.fixture(scope="function")
def test_event_counterparty():
    csv_files_written = {
        "counterparty": "counterparty/counterparty_2022-11-03 14_20_51.563000.csv",
    }
    timestamps_written = ["counterparty_timestamp.json"]
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

    @patch("src.week2_lambda.boto3")
    def test_fact_sales_event_input(
        self, mock_boto3, ingestion_bucket, test_event_input_sales_order
    ):
        # patch in s3 connection with filled ingestion bucket and empty processing bucket
        s3 = ingestion_bucket
        mock_boto3.client.return_value = s3
        # Run function
        output = lambda_handler(test_event_input_sales_order, {})
        # Collect output info and bucket contents
        pq_written = output["parquet_files_written"]
        response = s3.list_objects(Bucket="nc-terraformers-processing")
        content_list = [item["Key"] for item in response["Contents"]]
        # Assert output contains corresponding written file info that matches bucket contents
        assert list(pq_written.keys()) == ["fact_sales_order"]
        # Get resulting fact_sales_order parquet file from bucket and read into dataframe
        response = s3.get_object(
            Bucket="nc-terraformers-processing", Key=pq_written["fact_sales_order"]
        )
        body = response["Body"]
        pq = body.read()
        df = pd.read_parquet(BytesIO(pq))
        # Assert dataframe in correct fact_sales schema
        assert list(df.columns) == [
            "sales_order_id",
            "created_date",
            "created_time",
            "last_updated_date",
            "last_updated_time",
            "sales_staff_id",
            "counterparty_id",
            "units_sold",
            "unit_price",
            "currency_id",
            "design_id",
            "agreed_payment_date",
            "agreed_delivery_date",
            "agreed_delivery_location_id",
        ]

    @patch("src.week2_lambda.boto3")
    def test_address_input(self, mock_boto3, ingestion_bucket, test_event_address):
        # patch in s3 connection with filled ingestion bucket and empty processing bucket
        s3 = ingestion_bucket
        mock_boto3.client.return_value = s3
        # Run function
        output = lambda_handler(test_event_address, {})
        # Collect output info and bucket contents
        pq_written = output["parquet_files_written"]
        response = s3.list_objects(Bucket="nc-terraformers-processing")
        content_list = [item["Key"] for item in response["Contents"]]
        # Assert output contains corresponding written file info that matches bucket contents
        assert list(pq_written.keys()) == ["dim_location"]
        # Get resulting dim_location parquet file from bucket and read into dataframe
        response = s3.get_object(
            Bucket="nc-terraformers-processing", Key=pq_written["dim_location"]
        )
        body = response["Body"]
        pq = body.read()
        df = pd.read_parquet(BytesIO(pq))
        # Assert dataframe in correct fact_sales schema
        assert list(df.columns) == [
            "location_id",
            "address_line_1",
            "address_line_2",
            "district",
            "city",
            "postal_code",
            "country",
            "phone",
        ]

    @patch("src.week2_lambda.boto3")
    def test_currency_input(self, mock_boto3, ingestion_bucket, test_event_currency):
        # patch in s3 connection with filled ingestion bucket and empty processing bucket
        s3 = ingestion_bucket
        mock_boto3.client.return_value = s3
        # Run function
        output = lambda_handler(test_event_currency, {})
        # Collect output info and bucket contents
        pq_written = output["parquet_files_written"]
        response = s3.list_objects(Bucket="nc-terraformers-processing")
        content_list = [item["Key"] for item in response["Contents"]]
        # Assert output contains corresponding written file info that matches bucket contents
        assert list(pq_written.keys()) == ["dim_currency"]
        # Get resulting dim_currency parquet file from bucket and read into dataframe
        response = s3.get_object(
            Bucket="nc-terraformers-processing", Key=pq_written["dim_currency"]
        )
        body = response["Body"]
        pq = body.read()
        df = pd.read_parquet(BytesIO(pq))
        # Assert dataframe in correct fact_sales schema
        assert list(df.columns) == ["currency_id", "currency_code", "currency_name"]

    @patch("src.week2_lambda.boto3")
    def test_counterparty_input(
        self, mock_boto3, ingestion_bucket, test_event_counterparty
    ):
        # patch in s3 connection with filled ingestion bucket and empty processing bucket
        s3 = ingestion_bucket
        mock_boto3.client.return_value = s3
        # Run function
        output = lambda_handler(test_event_counterparty, {})
        # Collect output info and bucket contents
        pq_written = output["parquet_files_written"]
        response = s3.list_objects(Bucket="nc-terraformers-processing")
        content_list = [item["Key"] for item in response["Contents"]]
        # Assert output contains corresponding written file info that matches bucket contents
        assert list(pq_written.keys()) == ["dim_counterparty"]
        # Get resulting dim_counterparty parquet file from bucket and read into dataframe
        response = s3.get_object(
            Bucket="nc-terraformers-processing", Key=pq_written["dim_counterparty"]
        )
        body = response["Body"]
        pq = body.read()
        df = pd.read_parquet(BytesIO(pq))
        # Assert dataframe in correct fact_sales schema
        assert list(df.columns) == [
            "counterparty_id",
            "counterparty_legal_name",
            "counterparty_legal_address_line_1",
            "counterparty_legal_address_line_2",
            "counterparty_legal_district",
            "counterparty_legal_city",
            "counterparty_legal_postal_code",
            "counterparty_legal_country",
            "counterparty_phone_number",
        ]
