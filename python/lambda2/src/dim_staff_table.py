import boto3
import pandas as pd
from io import StringIO


def dim_staff():

    s3 = boto3.client("s3")
    ingested_bucket = 'nc-terraformers-ingestion'
    latest_data = s3.get_object(Bucket=ingested_bucket, Key=f"staff/**staff")
    pre_star_schema_df = pd.read_csv(StringIO(latest_data))
    star_schema_df = pre_star_schema_df[[
            "staff_id",
            "design_name",
            "file_location",
            "file_name"]].copy()


dim_staff()