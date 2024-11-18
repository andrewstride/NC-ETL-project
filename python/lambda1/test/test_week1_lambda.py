from src.week1_lambda import lambda_handler
from src.utils import (
    get_all_rows,
    get_columns,
    write_to_s3,
    get_tables,
    read_timestamp_from_s3,
    get_new_rows,
    write_df_to_csv,
    table_to_dataframe,
    timestamp_from_df,
    write_timestamp_to_s3,
)
from src.connection import db_connection, get_db_creds
from testfixtures import LogCapture
from moto import mock_aws
from unittest.mock import patch
import json
import boto3
import pytest
import pandas as pd
from datetime import datetime

@pytest.mark.skip
class TestGetDBCreds:
    def test_correct_keys_in_dict(self):
        creds = get_db_creds()
        keys = list(creds.keys())
        assert "username" in keys
        assert "password" in keys
        assert "host" in keys
        assert "port" in keys
        assert "dbname" in keys

    def test_values_are_strings(self):
        creds = get_db_creds()
        for cred in creds:
            assert isinstance(creds[cred], str)


class TestGetTables:
    def test_get_tables_returns_list(self):
        conn = db_connection()
        tables = get_tables(conn)
        assert isinstance(tables, list)

    def test_get_tables_returns_tables(self):
        conn = db_connection()
        tables = get_tables(conn)
        assert tables == [
            "sales_order",
            "transaction",
            "department",
            "staff",
            "purchase_order",
            "counterparty",
            "payment",
            "currency",
            "payment_type",
            "address",
            "design",
        ]


@pytest.mark.skip
class TestGetRows:
    def test_returns_list(self):
        conn = db_connection()
        assert isinstance(get_all_rows(conn, "staff"), list)

    def test_contains_lists(self):
        conn = db_connection()
        result = get_all_rows(conn, "staff")
        for row in result:
            assert isinstance(row, list)

    def test_correct_no_of_columns(self):
        conn = db_connection()
        result = get_all_rows(conn, "staff")
        for row in result:
            assert len(row) == 7

@pytest.mark.skip
class TestGetColumns:
    def test_returns_list(self):
        conn = db_connection()
        assert isinstance(get_columns(conn, "staff"), list)

    def test_correct_no_of_columns(self):
        conn = db_connection()
        result = get_columns(conn, "staff")
        assert len(result) == 7

@pytest.mark.skip("Test needs to be refactored.")
class TestLogger:
    @mock_aws
    def test_token_logger(self):
        with LogCapture() as l:
            lambda_handler([], {})
            l.check_present(("root", "ERROR", "Houston, we have a major problem"))

@pytest.mark.skip
class TestWriteToS3:
    @mock_aws
    def test_returns_dict(self):
        s3 = boto3.client("s3")
        data = json.dumps({"test": "data"})
        client = boto3.client("s3")
        client.create_bucket(
            Bucket="test-bucket",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        assert isinstance(
            write_to_s3(s3, "test-bucket", "test-file", "csv", data), dict
        )

    @mock_aws
    def test_writes_file(self):
        timestamp = ""
        s3 = boto3.client("s3")
        data = json.dumps({"test": "data"})
        client = boto3.client("s3")
        client.create_bucket(
            Bucket="test-bucket",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        output = write_to_s3(s3, "test-bucket", "test-file", "csv", data)
        objects = client.list_objects(Bucket="test-bucket")
        assert objects["Contents"][0]["Key"] == "test-file.csv"
        assert output["result"] == "Success"

    @mock_aws
    def test_handles_no_such_bucket_error(self):
        s3 = boto3.client("s3")
        data = json.dumps({"test": "data"})

        with LogCapture() as l:
            output = write_to_s3(s3, "non-existant-bucket", "test-file", "csv", data)
            assert output["result"] == "Failure"
            assert """root ERROR
  An error occurred (NoSuchBucket) when calling the PutObject operation: The specified bucket does not exist""" in (
                str(l)
            )

    @mock_aws
    def test_handles_filename_error(self):
        data = True
        client = boto3.client("s3")
        client.create_bucket(
            Bucket="test-bucket",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        with LogCapture() as l:
            output = write_to_s3(client, "test-bucket", "test-file", "csv", data)
            assert output["result"] == "Failure"
            assert """root ERROR
  Parameter validation failed:
Invalid type for parameter Body, value: True, type: <class 'bool'>, valid types: <class 'bytes'>, <class 'bytearray'>, file-like object""" in str(
                l
            )

@pytest.mark.skip
class TestReadTimestampFromS3:
    @mock_aws
    def test_returns_dict(self):
        s3 = boto3.client("s3")
        table = "staff"
        output = read_timestamp_from_s3(s3, table)
        assert isinstance(output, dict)

    @mock_aws
    def test_returns_timestamp_dict(self):
        s3 = boto3.client("s3")
        s3.create_bucket(Bucket="nc-terraformers-ingestion",
                         CreateBucketConfiguration={
                             "LocationConstraint": "eu-west-2"})
        data = json.dumps({"staff": "test_timestamp"})
        s3.put_object(Bucket="nc-terraformers-ingestion",
                      Body=data,
                      Key="staff_timestamp.json")
        table = "staff"
        output = read_timestamp_from_s3(s3, table)
        assert output == json.loads(data)

    @mock_aws
    def test_handles_no_timestamp(self):
        s3 = boto3.client("s3")
        s3.create_bucket(Bucket="nc-terraformers-ingestion",
                         CreateBucketConfiguration={
                             "LocationConstraint": "eu-west-2"})
        table = "staff"
        output = read_timestamp_from_s3(s3, table)
        assert output == {"detail" : "No timestamp exists"}

    @mock_aws
    def test_handles_error(self):
        s3 = boto3.client("s3")
        table = "staff"
        with LogCapture() as l:
            output = read_timestamp_from_s3(s3, table)
            assert output["result"] == "Failure"
            assert """root ERROR
  An error occurred (NoSuchBucket) when calling the GetObject operation: The specified bucket does not exist""" in str(
                l
            )

@pytest.mark.skip
class TestGetNewRows:
    def test_returns_list_of_lists(self):
        conn = db_connection()
        output = get_new_rows(conn, "staff", "2013-11-14 10:19:09.990000")
        assert isinstance(output, list)
        for item in output:
            assert isinstance(item, list)

    def test_handles_incorrect_timestamp(self):
        conn = db_connection()
        with LogCapture() as l:
            output = get_new_rows(conn, "staff", "incorrect timestamp")
            assert '''{'S': 'ERROR', 'V': 'ERROR', 'C': '22007', 'M': 'invalid value "inco" for "YYYY"', 'D': 'Value must be an integer.', 'F': 'formatting.c', 'L': '2416', 'R': 'from_char_parse_int_len'}''' in str(l)
        assert output == []

    def test_returns_data_after_timestamp(self):
        timestamp = "2024-11-14 12:37:09.990000"
        conn = db_connection()
        output = get_new_rows(conn, "sales_order", timestamp)
        columns = get_columns(conn, "sales_order")
        df = pd.DataFrame(output, columns=columns)
        print(str(df["last_updated"].min()))
        format_string = "%Y-%m-%d %H:%M:%S.%f"
        min_time = df["last_updated"].min().to_pydatetime()
        assert min_time >= datetime.strptime(timestamp,
                                             format_string)
        assert type(min_time) == type(datetime.strptime(timestamp,
                                             format_string))

    def test_handles_invalid_table_name(self):
        conn = db_connection()
        table = "invalid"
        timestamp = "2024-11-14 12:37:09.990000"
        with LogCapture() as l:
            output = get_new_rows(conn, table, timestamp)
            assert output == []
            assert "root ERROR\n  Table not found" in str(l)

    def test_handles_error(self):
        conn = db_connection()
        table = "staff"
        timestamp = "hello"
        with LogCapture() as l:
            output = get_new_rows(conn, table, timestamp)
            assert output == []
            assert "root ERROR" in str(l)


class TestWriteDfToCsv:
    def test_returns_a_dict_with_result_key(self):
        conn = db_connection()
        test_rows = get_all_rows(conn, "staff")
        test_columns = get_columns(conn, "staff")
        test_df = pd.DataFrame(test_rows, columns=test_columns)
        test_name = "staff"
        with mock_aws():
            client = boto3.client("s3")
            test_bucket = "nc-terraformers-ingestion"
            client.create_bucket(
                Bucket=test_bucket,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
            )
            output = write_df_to_csv(client, test_df, test_name)
            assert isinstance(output, dict)
            assert isinstance(output["result"], str)
    
    def test_converts_data_to_csv_and_uploads_to_s3_bucket(self):
        conn = db_connection()
        test_rows = get_all_rows(conn, "staff")
        test_columns = get_columns(conn, "staff")
        test_df = pd.DataFrame(test_rows, columns=test_columns)
        test_name = "staff"
        with mock_aws():
            client = boto3.client("s3")
            test_bucket = "nc-terraformers-ingestion"
            client.create_bucket(
                Bucket=test_bucket,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
            )
            write_df_to_csv(client, test_df, test_name)
            response = client.list_objects_v2(Bucket=test_bucket).get("Contents")
            bucket_files = [file["Key"] for file in response]
            if len(bucket_files) > 1:
                get_file = client.get_object(Bucket=test_bucket, Key=test_name)
                assert get_file["ContentType"] == "csv"
    
    def test_uploads_to_s3_bucket(self):
        conn = db_connection()
        test_rows = get_all_rows(conn, "staff")
        test_columns = get_columns(conn, "staff")
        test_df = pd.DataFrame(test_rows, columns=test_columns)
        test_name = "staff"
        with mock_aws():
            client = boto3.client("s3")
            test_bucket = "nc-terraformers-ingestion"
            client.create_bucket(
                Bucket=test_bucket,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
            )
            output = write_df_to_csv(client, test_df, test_name)
            assert output == {
                "result": "Success",
                "detail": "Converted to csv, uploaded to ingestion bucket",
            }
            response = client.list_objects_v2(Bucket=test_bucket).get("Contents")
            bucket_files = [file["Key"] for file in response]
            for file in bucket_files:
                assert "staff/staff" in file
                assert ".csv" in file
   
    def test_handles_error(self):
        with mock_aws():
            test_df = ""
            test_name = ""
            client = boto3.client("s3")
            test_bucket = "nc-terraformers-ingestion"
            client.create_bucket(
                Bucket=test_bucket,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
            )
            with LogCapture() as l:
                output = write_df_to_csv(client, test_df, test_name)
                assert output == {"result": "Failure"}
                assert "'str' object has no attribute 'to_csv'" in str(l)


class TestTableToDataframe:
    def test_makes_data_frame_from_rows_and_columns(self):
        conn = db_connection()
        test_rows = get_all_rows(conn, "staff")
        test_columns = get_columns(conn, "staff")
        output = table_to_dataframe(test_rows, test_columns)
        assert isinstance(output, pd.DataFrame)

    # def test_handles_error(self):
    #     test_rows = ""
    #     test_columns = ""
    #     with LogCapture() as l:
    #         output = table_to_dataframe(test_rows, test_columns)
    #         assert output == {"result": "Failure"}
    #         assert "DataFrame constructor not properly called!" in str(l)


class TestTimestampFromDf:
    def test_calculates_max_last_updated_timestamp_in_dataframe(self):
        test_rows = [[True, datetime(2022, 11, 3, 14, 20, 51, 563000)],
                     [True, datetime(2023, 11, 3, 14, 20, 51, 563000)]]
        test_columns = ["column1", "last_updated"]
        test_df = pd.DataFrame(test_rows, columns=test_columns)
        expected_as_datetime = datetime(2023, 11, 3, 14, 20, 51, 563000)
        output = timestamp_from_df(test_df)
        assert output.to_pydatetime() == expected_as_datetime

@pytest.mark.skip
class TestLambdaHandler:
    # @mock_aws
    def test_returns_200_response(self):
        client = boto3.client("s3")
        # client.create_bucket(Bucket='nc-terraformers-ingestion', CreateBucketConfiguration={
        # 'LocationConstraint': 'eu-west-2'})
        output = lambda_handler({}, {})
        assert output == {"response": 200}
        response = client.list_objects(Bucket="nc-terraformers-ingestion")
        for item in response["Contents"]:
            print(item["Key"])
        assert response == 1


# class TestGetTimestampFromDataFrame:
#     def test_returns_timestamp(self):
#         conn = db_connection()
#         rows = get_all_rows(conn, "sales_order")
#         columns = get_columns(conn, "sales_order")
#         test_df = pd.DataFrame(rows, columns=columns)
#         #print(test_df['last_updated'].max())
#         test_df.head().to_json('test_table.json')

# @pytest.mark.skip
# class TestReadTimestampFromS3:
    
#     @mock_aws
#     def test_(self):
#         table = "staff"
#         s3 = boto3.client("s3")
#         s3.create_bucket(Bucket="nc-terraformers-ingestion",
#                          CreateBucketConfiguration={
#                              "LocationConstraint": "eu-west-2"})
#         output = read_timestamp_from_s3(s3, table)
#         print(output)
#         assert output == 1