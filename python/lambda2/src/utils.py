import json
import boto3

def read_data_from_s3_bucket():
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    ingested_bucket = 'nc-terraformers-ingestion'
    return ingested_bucket


    # pre_star_schema_df = pd.read_csv(StringIO(latest_data))
    # star_schema_df = pre_star_schema_df[[
    #         "design_id",
    #         "design_name",
    #         "file_location",
    #         "file_name"]].copy()
    #input bucket to read data from the s3 bucket
    #perfom dimensional table process
    #convert to parquet
    #write to output s3 bucket