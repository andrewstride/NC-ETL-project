from src.dim_design import dim_design
from testconf import processing_bucket, ingestion_bucket
from unittest.mock import patch
from testfixtures import LogCapture
import pandas as pd
from io import BytesIO

class TestDimDesign:
    @patch("src.dim_design.datetime")
    def test_uploads_parquet_object_to_processing_bucket(self,
                                                         mock_datetime,
                                                         ingestion_bucket,
                                                         processing_bucket
                                                         ):
        mock_datetime.now.return_value = "timestamp"
        output = dim_design(processing_bucket)
        assert output == {"result": "Success"}

        expected_name = "dim_design/dim_design_timestamp.parquet"
        test_bucket = "nc-terraformers-processing"
        response = processing_bucket.list_objects_v2(Bucket=test_bucket).get("Contents")
        bucket_files = [file["Key"] for file in response]
        assert expected_name in bucket_files

    def test_handles_error(self,
                           processing_bucket):
        with LogCapture() as l:
            output = dim_design(processing_bucket)
            assert output == {"result": "Failure"}
            assert "The specified bucket does not exist" in str(l)

    @patch("src.dim_design.datetime")
    def test_parquet_contains_correct_data(self,
                                           mock_datetime,
                                           processing_bucket,
                                           ingestion_bucket):
        mock_datetime.now.return_value = "timestamp"
        output = dim_design(processing_bucket)

        parquet_file = processing_bucket.get_object(
            Bucket="nc-terraformers-processing",
            Key="dim_design/dim_design_timestamp.parquet")
        
        df = pd.read_parquet(BytesIO(parquet_file['Body'].read()))
        assert list(df.columns) == ["design_id",
                                    "design_name",
                                    "file_location",
                                    "file_name"]
        assert list(df.iloc[0]) == [1,
                                    "Steel",
                                    "/private",
                                    "steel-20220717-npgz.json"]
