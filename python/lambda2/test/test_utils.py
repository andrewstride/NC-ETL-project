from testfixtures import LogCapture
from src.utils import collate_csv_into_df, split_timestamp
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
        assert len(staff_df) == 475


class TestSplitTimestamp:
    def test_returns_date(self):
        output = split_timestamp("2024-12-01 15:32:10.242324")
        assert output[0] == "2024-12-01"

    def test_returns_time(self):
        output = split_timestamp("2024-12-01 15:32:10.242324")
        assert output[1] == "15:32:10.242324"
