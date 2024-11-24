from src.convert_to_parquet_and_upload import (
    convert_to_parquet,
    upload_to_processing_bucket,
)
import pandas as pd
from io import BytesIO
from unittest.mock import patch
from testfixtures import LogCapture


class TestConvertToParquet:
    def test_output_is_parquet(self):
        data = [["a1", "b1"], ["a2", "b2"], ["a3", "b3"]]
        input_df = pd.DataFrame(data, columns=["col1", "col2"])
        output = convert_to_parquet(input_df)
        parquet_as_df = pd.read_parquet(BytesIO(output.getvalue()))
        assert list(parquet_as_df.columns) == ["col1", "col2"]
        assert list(parquet_as_df.iloc[0]) == ["a1", "b1"]
        assert list(parquet_as_df.iloc[1]) == ["a2", "b2"]
        assert list(parquet_as_df.iloc[2]) == ["a3", "b3"]

    def test_handles_a_non_df_object_as_error(self):
        output = convert_to_parquet("")
        assert output == {"result": "Failure"}


class TestUploadToProcessingBucket:
    @patch("src.convert_to_parquet_and_upload.datetime")
    def test_uploads_parquet_to_processing_bucket(
        self, mock_datetime, processing_bucket, test_parquet
    ):
        mock_datetime.now.return_value = "timestamp"
        table_name = "dim_design"
        output = upload_to_processing_bucket(
            processing_bucket, test_parquet, table_name
        )
        assert output == {"dim_design": "dim_design/dim_design_timestamp.parquet"}

        expected_name = "dim_design/dim_design_timestamp.parquet"
        test_bucket = "nc-terraformers-processing"
        response = processing_bucket.list_objects_v2(Bucket=test_bucket).get("Contents")
        bucket_files = [file["Key"] for file in response]
        assert expected_name in bucket_files

    @patch("src.convert_to_parquet_and_upload.datetime")
    def test_parquet_contains_correct_data(
        self, mock_datetime, processing_bucket, test_parquet
    ):
        mock_datetime.now.return_value = "timestamp"
        table_name = "dim_design"
        upload_to_processing_bucket(processing_bucket, test_parquet, table_name)
        parquet_file = processing_bucket.get_object(
            Bucket="nc-terraformers-processing",
            Key="dim_design/dim_design_timestamp.parquet",
        )
        df = pd.read_parquet(BytesIO(parquet_file["Body"].read()))
        assert list(df.columns) == ["col1", "col2"]
        assert list(df.iloc[0]) == ["a1", "b1"]
        assert list(df.iloc[1]) == ["a2", "b2"]
        assert list(df.iloc[2]) == ["a3", "b3"]

    @patch("src.convert_to_parquet_and_upload.datetime")
    def test_handles_no_dataframe_error(self, mock_datetime, processing_bucket):
        with LogCapture() as log:
            mock_datetime.now.return_value = "timestamp"
            table_name = "dim_design"
            output = upload_to_processing_bucket(processing_bucket, "", table_name)
            assert output == {"result": "Failure"}
            assert "ERROR" in str(log)

    @patch("src.convert_to_parquet_and_upload.datetime")
    def test_handles_no_bucket_error(self, mock_datetime, test_parquet):
        with LogCapture() as log:
            mock_datetime.now.return_value = "timestamp"
            table_name = "dim_design"
            output = upload_to_processing_bucket("", test_parquet, table_name)
            assert output == {"result": "Failure"}
            assert "ERROR" in str(log)

    @patch("src.convert_to_parquet_and_upload.datetime")
    def test_handles_non_existant_table_name(
        self, mock_datetime, test_parquet, processing_bucket
    ):
        with LogCapture() as log:
            mock_datetime.now.return_value = "timestamp"
            output = upload_to_processing_bucket(processing_bucket, test_parquet, "")
            assert output == {"result": "Failure"}
            assert "Invalid table name." in str(log)
