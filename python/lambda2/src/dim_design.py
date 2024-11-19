from datetime import datetime
import json
import pandas as pd
from io import BytesIO, StringIO
import logging


def dim_design(s3):
    try:
        timestamp = datetime.now()
        ingestion_bucket = "nc-terraformers-ingestion"
        processing_bucket = "nc-terraformers-processing"

        latest_timestamp_json = s3.get_object(
            Bucket=ingestion_bucket,
            Key="design_timestamp.json")
        latest_timestamp = json.loads(latest_timestamp_json[
            "Body"].read().decode("utf-8"))["design"]

        latest_data = s3.get_object(
            Bucket=ingestion_bucket,
            Key=f"design/design_{latest_timestamp}.csv"
        )["Body"].read().decode("utf-8")

        pre_star_schema_df = pd.read_csv(StringIO(latest_data))
        star_schema_df = pre_star_schema_df[[
            "design_id",
            "design_name",
            "file_location",
            "file_name"]].copy()

        out_buffer = BytesIO()
        star_schema_df.to_parquet(out_buffer, index=False)
        s3.put_object(
            Bucket=processing_bucket,
            Body=out_buffer.getvalue(),
            Key=f"dim_design/dim_design_{timestamp}.parquet")
        return {"result": "Success"}
    except Exception as e:
        logging.error(e)
        return {"result": "Failure"}
