from src.dim_design import dim_design
from testconf import aws_cred, processed_bucket, ingestion_bucket#, ingestion_bucket_with_objects
from unittest.mock import patch


class TestDimDesign:
    @patch("src.dim_design.datetime")
    def test_uploads_parquet_object_to_processed_bucket(self, mock_datetime,
                                                        processed_bucket,
                                                        ingestion_bucket):
        s3 = processed_bucket
        s3.upload_file("test/design_timestamp.json","nc-terraformers-ingestion", "design_timestamp.json")
        s3.upload_file("test/design_2024-11-18 10_56_09.970000.csv", "nc-terraformers-ingestion","design/design_2024-11-18 10:56:09.970000.csv")
        mock_datetime.now.return_value = "timestamp"

        dim_design(s3)

        expected_name = "dim_design/dim_design_timestamp.parquet"
        test_bucket = "nc-terraformers-processing"
        response = s3.list_objects_v2(Bucket=test_bucket).get("Contents")
        bucket_files = [file["Key"] for file in response]
        print(bucket_files)
        assert expected_name in bucket_files