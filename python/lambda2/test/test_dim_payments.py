from src.dim_payments_table import dim_new_staff
import pytest
import boto3
import pandas as pd

s3 = boto3.client("s3")
class TestData:
    def test_dim_table_dictionary(self):
        test = dim_new_staff(s3)
        assert isinstance(test, pd.DataFrame)

    def test_dim_date_table_length(self):
        test = dim_new_staff(s3)
# want to write some mock tests     
        