from src.lambda3_utils import import_pq_to_df, df_to_sql
from src.lambda3_connection import wh_connection
import boto3
import logging

logger = logging.getLogger()
logger.setLevel("INFO")


def lambda_handler(event, context):
    """
        Event input:
    {"response": 200,
    "parquet_files_written": {table_name: parquet_files_written,
                                table_name2: pq file 2}
                                }
    """
    try:
        logging.info("Connecting to Processing Bucket")
        s3 = boto3.client("s3")
        logging.info("Connecting to Data Warehouse")
        conn = wh_connection()
        logging.info("Collecting file info from Transform Lambda")
        files_written_dict = event["parquet_files_written"]
        for key in files_written_dict:
            df = import_pq_to_df(s3, files_written_dict[key])
            df_to_sql(df, key, conn)
        return {"response": 200}

    except Exception as e:
        logging.error(e)
        return {"error": e}
