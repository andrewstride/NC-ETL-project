import os
import pytest
import boto3
import pandas as pd
from pg8000.native import Connection
from io import BytesIO
from datetime import datetime
from moto import mock_aws
from src.lambda3_connection import wh_connection


@pytest.fixture(scope="function")
def aws_cred():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def test_dim_df():
    rows = [
        [
            1,
            "Jeremie",
            "Franey",
            "Sales",
            "Manchester",
            "jeremie.franey@terrifictotes.com",
        ],
        [2, "Deron", "Beier", "Marketing", "Leeds", "deron.beier@terrifictotes.com"],
        [
            3,
            "Jeanette",
            "Erdman",
            "Finance",
            "York",
            "jeanette.erdman@terrifictotes.com",
        ],
    ]
    cols = [
        "staff_id",
        "first_name",
        "last_name",
        "department_name",
        "location",
        "email_address",
    ]
    return pd.DataFrame(rows, columns=cols)


@pytest.fixture(scope="function")
def nc_terraformers_processing_s3(test_dim_df):
    out_buffer = BytesIO()
    test_dim_df.to_parquet(out_buffer, index=False)
    test_parq = out_buffer.getvalue()
    with mock_aws():
        s3 = boto3.client("s3")
        test_bucket = "nc-terraformers-processing"
        s3.create_bucket(
            Bucket=test_bucket,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        s3.put_object(Bucket=test_bucket, Body=test_parq, Key="test_staff.parquet")
        yield s3


@pytest.fixture(scope="function")
def conn_fixture():
    conn = Connection(
        "andrewstride",
        password="",
        database="test_warehouse",
        host="localhost",
        port=5432,
    )
    return conn


@pytest.fixture(scope="function")
def mock_event():
    return {
        "response": 200,
        "parquet_files_written": {"dim_staff": "test_staff.parquet"},
    }
