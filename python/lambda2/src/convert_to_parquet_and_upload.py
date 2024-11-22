from io import BytesIO
import logging
from datetime import datetime


def convert_to_parquet(df):
    """Takes a DataFrame and converts it
    to a parquet buffer object

    Paramaters:
        df: a pandas DataFrame

    Returns:
        A parquet buffer of the DataFrame, if successful
        OR
        Dict (dict): {"result": "Failure"}, if unsuccessful
    """
    try:
        out_buffer = BytesIO()
        df.to_parquet(out_buffer, index=False)
        return out_buffer
    except Exception:
        return {"result": "Failure"}


def upload_to_processing_bucket(s3, parq_buffer, table_name):
    """Takes a s3 client, parquet buffer, and a table name,
    and uploads the parquet object to the processing bucket

    Paramaters:
        s3: Boto3.client('s3') connection
        parq_buffer: a parquet buffer object
        table_name (str): the name of a table for the star_schema

    Returns:
        Dict (dict): {"result": "Failure/Success"}
    """
    tables = [
        "dim_date",
        "dim_staff",
        "dim_counterparty",
        "dim_currency",
        "dim_design",
        "dim_location",
        "fact_sales_order",
    ]
    if table_name in tables:
        try:
            timestamp = datetime.now()
            s3.put_object(
                Bucket="nc-terraformers-processing",
                Body=parq_buffer.getvalue(),
                Key=f"{table_name}/{table_name}_{timestamp}.parquet",
            )
            return {"result": "Success"}
        except Exception as e:
            logging.error(e)
    else:
        logging.error("Invalid table name.")
    return {"result": "Failure"}
