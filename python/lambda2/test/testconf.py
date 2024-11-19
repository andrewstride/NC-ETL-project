from moto import mock_aws
import boto3
import pytest
import os

@pytest.fixture(scope="function")
def aws_cred():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

@pytest.fixture(scope="function")
def processed_bucket():
    with mock_aws():
        s3 = boto3.client("s3")
        test_bucket = "nc-terraformers-processing"
        s3.create_bucket(
            Bucket=test_bucket,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        yield s3

@pytest.fixture()
def ingestion_bucket():
    with mock_aws():
        s3 = boto3.client("s3")
        test_bucket = "nc-terraformers-ingestion"
        s3.create_bucket(
            Bucket=test_bucket,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        yield s3

# @pytest.fixture()
# def ingestion_bucket_with_objects(ingestion_bucket):
#     s3 = ingestion_bucket
#     bucket_name = "nc-terraformers-ingestion"

#     ''' Make file1 '''
#     with open('file1.txt', 'w', encoding='utf-8') as file:
#         file.write("Text of file1!")
#         file1_name = 'design/design_2024-11-18 16:53:23.353536.csv'
#     s3.upload_file('file1.txt', bucket_name, file1_name)

#     ''' Make file2 '''
#     with open('file2.txt', 'w', encoding='utf-8') as file:
#         file.write("Text of file2!")
#         file2_name = 'design/design_2024-11-18 19:15:01.821957.csv'
#     s3.upload_file('file2.txt', bucket_name, file2_name)

#     ''' Make file3 '''
#     with open('file3.txt', 'w', encoding='utf-8') as file:
#         file.write("Text of file3!")
#         file3_name = 'not a design table!.csv'
#     s3.upload_file('file3.txt', bucket_name, file3_name)

#     yield s3