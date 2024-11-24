import pandas as pd
import json
from io import StringIO
import logging


def get_latest_file_as_df(s3, table_name):
    """Takes a s3 client and a table name, retrieves the
    latest file of that table from the ingestion bucket,
    and returns the data as a DataFrame

    Paramaters:
        s3: Boto3.client('s3') connection
        table_name (str): the name of a table for the star_schema

    Returns:
        DataFrame: of the latest data of the given table
        Dict (dict): {"result": "Failure"} if unsuccessful
    """
    try:
        """Get latest timestamp for table from timestamp JSON"""
        latest_timestamp_json = s3.get_object(
            Bucket="nc-terraformers-ingestion", Key=f"{table_name}_timestamp.json"
        )
        latest_timestamp = json.loads(
            latest_timestamp_json["Body"].read().decode("utf-8")
        )[table_name]

        """ Get latest file of table """
        latest_data = (
            s3.get_object(
                Bucket="nc-terraformers-ingestion",
                Key=f"{table_name}/{table_name}_{latest_timestamp}.csv",
            )["Body"]
            .read()
            .decode("utf-8")
        )

        """ Return DataFrame of data from latest file """
        return pd.read_csv(StringIO(latest_data))

    except Exception as e:
        logging.error(e)
        return {"result": "Failure"}
