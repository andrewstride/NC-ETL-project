from testfixtures import LogCapture
from src.utils import collate_csv_into_df, split_timestamp, check_for_dim_date
import pandas as pd
import pytest


class TestCollateCSVtoDF:
    def test_returns_dataframe(self, ingestion_bucket):
        assert isinstance(collate_csv_into_df(ingestion_bucket, "design"), pd.DataFrame)

    def test_df_data_merged(self, ingestion_bucket):
        design_df = collate_csv_into_df(ingestion_bucket, "design")
        no_of_rows = len(design_df)
        assert no_of_rows == 950

    def test_handles_no_files(self, ingestion_bucket):
        with LogCapture() as l:
            response = collate_csv_into_df(ingestion_bucket, "invalid")
            assert response == None
            assert "Encountered error gathering invalid files:" in str(l)
            assert "No objects to concatenate" in str(l)

    def test_gathers_single_file(self, ingestion_bucket):
        staff_df = collate_csv_into_df(ingestion_bucket, "staff")
        assert len(staff_df) == 20


class TestSplitTimestamp:
    def test_returns_date(self):
        output = split_timestamp("2024-12-01 15:32:10.242324")
        assert output[0] == "2024-12-01"

    def test_returns_time(self):
        output = split_timestamp("2024-12-01 15:32:10.242324")
        assert output[1] == "15:32:10"


class TestCheckForDimDate:
    def test_returns_bool(self, processing_bucket):
        assert isinstance(check_for_dim_date(processing_bucket), bool)

    def test_returns_false_on_empty(self, processing_bucket):
        assert check_for_dim_date(processing_bucket) == False

    def test_returns_true_if_dim_date_present(self, processing_bucket):
        processing_bucket.put_object(
            Bucket="nc-terraformers-processing",
            Body="test",
            Key="dim_date/dim_date_1234.parquet",
        )
        assert check_for_dim_date(processing_bucket) == True

    def test_progress_logged(self, processing_bucket):
        with LogCapture() as l:
            check_for_dim_date(processing_bucket)
            assert "Checking for dim_date file in processing bucket" in str(l)
            assert "dim_date file not found" in str(l)
            processing_bucket.put_object(
                Bucket="nc-terraformers-processing",
                Body="test",
                Key="dim_date/dim_date_1234.parquet",
            )
            check_for_dim_date(processing_bucket)
            assert "dim_date file found: dim_date/dim_date_1234.parquet"
