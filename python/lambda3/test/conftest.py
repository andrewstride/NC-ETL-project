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
def test_df():
    rows = [
        [
            1,
            "Jeremie",
            "Franey",
            2,
            "jeremie.franey@terrifictotes.com",
            datetime(2022, 11, 3, 14, 20, 51, 563000),
            datetime(2022, 11, 3, 14, 20, 51, 563000),
        ],
        [
            2,
            "Deron",
            "Beier",
            6,
            "deron.beier@terrifictotes.com",
            datetime(2022, 11, 3, 14, 20, 51, 563000),
            datetime(2022, 11, 3, 14, 20, 51, 563000),
        ],
        [
            3,
            "Jeanette",
            "Erdman",
            6,
            "jeanette.erdman@terrifictotes.com",
            datetime(2022, 11, 3, 14, 20, 51, 563000),
            datetime(2022, 11, 3, 14, 20, 51, 563000),
        ],
    ]
    cols = [
        "staff_id",
        "first_name",
        "last_name",
        "department_id",
        "email_address",
        "created_at",
        "last_updated",
    ]
    return pd.DataFrame(rows, columns=cols)

@pytest.fixture(scope="function")
def nc_terraformers_processing_s3(test_df):
    out_buffer = BytesIO()
    test_df.to_parquet(out_buffer, index=False)
    test_parq = out_buffer.getvalue()
    with mock_aws():
        s3 = boto3.client("s3")
        test_bucket = "nc-terraformers-processing"
        s3.create_bucket(
            Bucket=test_bucket,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        s3.put_object(
            Bucket=test_bucket,
            Body=test_parq,
            Key="test_staff.parquet")
        yield s3




@pytest.fixture(scope="function")
def conn_fixture():
    conn = Connection(
        "testuser",
        password="testuser",
        database="test-warehouse",
        host="localhost",
        port=5432,
    )
    return conn