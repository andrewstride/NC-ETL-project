import boto3
from src.dim_date_table import dim_date_table

class Test_reading_data:
    def test_reading_data_from_s3_ingestion(self):
        test = dim_date_table()
        print(test)
        assert isinstance(test, list)
       