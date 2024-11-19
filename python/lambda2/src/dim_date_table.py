from datetime import datetime
from pprint import pprint
import pandas
import boto3


def dim_date_table():
    s3_client = boto3.client("s3")
    bucket_name = "nc-terraformers-ingestion"
    list_object = s3_client.list_objects_v2(Bucket=bucket_name).get("Contents")
    # creates a list of all the csv files
    csv_list = [obj['Key'] for obj in list_object if obj['Key'].endswith('.csv')]
    # for obj in list_object:
    #     if obj['Key'].endswith('.csv'):
    #         csv_list.append(obj['Key'])
        # print(f"file_name: {obj['Key']}")
    return csv_list

