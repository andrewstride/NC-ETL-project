import json
import boto3

def read_data_from_s3_bucket():
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    ingested_bucket = response['Buckets'][1]['Name']
    return ingested_bucket
    


    #input bucket to read data from the s3 bucket
    #perfom dimensional table process
    #convert to parquet
    #write to output s3 bucket