import boto3
from datetime import datetime
import json
import pandas as pd
from io import BytesIO, StringIO
import logging
from ast import literal_eval

s3 = boto3.client("s3")
def dim_staff(s3):

    try:
        """
        collecting the latest timestamp for staff and department tables from s3 bucket
        """
        timestamp = datetime.now()
        ingestion_bucket = "nc-terraformers-ingestion"
        latest_timestamp_json = s3.get_object(
            Bucket=ingestion_bucket,
            Key="staff_timestamp.json"
        )
        latest_timestamp_department_json = s3.get_object(
            Bucket=ingestion_bucket,
            Key="department_timestamp.json"
        )
        """
        
        """
        latest_timestamp = json.loads(latest_timestamp_json["Body"].read().decode("utf-8"))["staff"]
        latest_department_timestamp = json.loads(latest_timestamp_department_json["Body"].read().decode("utf-8"))["department"]

        latest_data = s3.get_object(
            Bucket=ingestion_bucket,
            Key=f"staff/staff_{latest_timestamp}.csv"
        )["Body"].read().decode("utf-8")

        department_data = s3.get_object(
            Bucket=ingestion_bucket,
            Key=f"department/department_{latest_department_timestamp}.csv"
        )["Body"].read().decode("utf-8")
        """
        
        """
        df_staff = pd.read_csv(StringIO(latest_data))
        df_department = pd.read_csv(StringIO(department_data))

        staff_department = pd.concat([df_staff, df_department])
        staff_department_str = str(staff_department)
        df["Hello"] = staff_department_str[["department_id", "department_name"]].agg("-"join(), axis=1)
        return df["Hello"]


    

        # star_schema_df = staff_department[[
        #     "staff_id",
        #     "first_name",
        #     "last_name",
        #     "department_name",
        #     "location",
        #     "email_address"
        # ]].copy()
        # return star_schema_df
    except Exception as e:
        logging.error(e)
        return {"result": "Failure"}
print(dim_staff(s3))