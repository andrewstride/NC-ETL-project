import pandas as pd
import json
from io import StringIO
import logging
from pprint import pprint

def get_latest_file(s3, table_name):
    try:
        ''' Get latest timestamp for table
        from timestamp JSON
        '''
        latest_timestamp_json = s3.get_object(
            Bucket="nc-terraformers-ingestion",
            Key=f"{table_name}_timestamp.json")
        latest_timestamp = json.loads(latest_timestamp_json[
            "Body"].read().decode("utf-8"))["design"]

        ''' Get the latest file for table
         from the latest timestamp
        '''
        latest_data = s3.get_object(
            Bucket="nc-terraformers-ingestion",
            Key=f"{table_name}/{table_name}_{latest_timestamp}.csv"
        )["Body"].read().decode("utf-8")

        ''' Return DataFrame of file'''
        return pd.read_csv(StringIO(latest_data))
    
    except Exception as e:
        logging.error(e)
        return {"result": "Failure"}


# def extract_file_to_df(s3, file_name):
#     try:
#         latest_data = s3.get_object(
#                 Bucket="nc-terraformers-ingestion",
#                 Key=file_name
#             )["Body"].read().decode("utf-8")
#         return pd.read_csv(StringIO(latest_data))
#     except Exception as e:
#         logging.error(e)
#         return {"result": "Failure"}