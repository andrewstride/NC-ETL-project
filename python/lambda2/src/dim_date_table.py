from datetime import datetime
from pprint import pprint
import boto3


def dim_date_table():
    s3_client = boto3.client("s3")
    bucket_name = "nc-terraformers-ingestion"
    list_object = s3_client.list_objects_v2(Bucket=bucket_name).get("Contents")
    for obj in list_object:
        # print(f"file_name: {obj['Key']}")
        return obj
