from src.week3_lambda import lambda_handler
from src.utils import get_parquet
from testfixtures import LogCapture
import pandas as pd

class TestGetParquet:
    def test_returns_dataframe(self, nc_terraformers_processing_s3):
        output = get_parquet(nc_terraformers_processing_s3, "test_staff.parquet")
        assert isinstance(output, pd.DataFrame)

    def test_df_unchanged(self, nc_terraformers_processing_s3, test_df):
        output = get_parquet(nc_terraformers_processing_s3, "test_staff.parquet")
        assert output.equals(test_df)

    def test_handles_no_such_key_error(self, nc_terraformers_processing_s3):
        with LogCapture() as l:
            output = get_parquet(nc_terraformers_processing_s3, "invalid_file.parquet")
            assert output == {"result": "failure"}
            assert "An error occurred (NoSuchKey) when calling the GetObject operation: The specified key does not exist." in str(l)

    def test_logs_progress(self, nc_terraformers_processing_s3):
        with LogCapture() as l:
            get_parquet(nc_terraformers_processing_s3, "test_staff.parquet")
            assert "Reading test_staff.parquet from nc-terraformers-processing bucket" in str(l)
            assert "test_staff.parquet file successfully imported into DataFrame" in str(l)