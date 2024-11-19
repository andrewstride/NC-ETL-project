import boto3
import pytest

from src.utils import read_data_from_s3_bucket

def test_check_bucket():
    test = read_data_from_s3_bucket()
    print(test)
    assert test == 'nc-terraformers-ingestion'
