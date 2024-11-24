import pandas as pd
import json
from io import StringIO
import logging


def get_latest_file_as_df(s3, file_name):
    """Takes a s3 client and a file name, retrieves the
    file from the ingestion bucket,
    and returns the data as a DataFrame

    Args:
        s3: Boto3.client('s3') connection
        filename (str): the file to collect from s3

    Returns:
        DataFrame: of the latest data of the given table
        Dict (dict): {"result": "Failure"} if unsuccessful
    """
    try:
        """Get latest file of table"""
        latest_data = (
            s3.get_object(
                Bucket="nc-terraformers-ingestion",
                Key=file_name,
            )["Body"]
            .read()
            .decode("utf-8")
        )

        """ Return DataFrame of data from latest file """
        return pd.read_csv(StringIO(latest_data))

    except Exception as e:
        logging.error(e)
        return {"result": "Failure"}
