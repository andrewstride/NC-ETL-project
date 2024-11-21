from src.week3_lambda import lambda_handler
from src.utils import get_parquet
import pandas as pd

class TestGetParquet:
    def test_returns_dataframe(self, nc_terraformers_processing_s3):
        output = get_parquet(nc_terraformers_processing_s3, "test_staff.parquet")
        assert isinstance(output, pd.DataFrame)