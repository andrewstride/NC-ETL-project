import pandas as pd
import logging
from src.get_latest_file_as_df import get_latest_file_as_df


def collate_csv_into_df(s3, table_name):
    """Gathers all csv files for given table

    Args:
        s3 (boto3.client('s3')): s3 client connection
        table_name (string): Table to be collected

    Returns:
        Pandas DataFrame
    """
    try:
        # list objects in s3
        response = s3.list_objects(Bucket="nc-terraformers-ingestion")
        content_list = [item["Key"] for item in response["Contents"]]
        # make list of all filenames that begin with table_name/table_name
        prefix = f"{table_name}/{table_name}"
        collect_list = []
        for item in content_list:
            if prefix in item:
                collect_list.append(item)
        # collect all of these files as dataframes
        logging.info(f"Collecting {table_name} files")
        df_list = []
        for filename in collect_list:
            logging.info(f"collecting {filename} from s3")
            df = get_latest_file_as_df(s3, filename)
            df_list.append(df)
        # merge dataframes together
        merged_df = pd.concat(df_list)
        logging.info(f"{table_name} table concatenated")
        # return dataframe
        return merged_df
    except Exception as e:
        logging.error(f"Encountered error gathering {table_name} files: {e}")


def split_timestamp(timestamp):
    """Splits timestamp into date and time

    Args:
        timestamp (timestamp): YYYY-MM-DD HH:MM:SS.US

    Returns: [date, time]
    """
    return [timestamp[:10], timestamp[11:]]


def check_for_dim_date(s3):
    """Checks if dim_date present in processing bucket
    Args:
        s3 (boto3.client('s3')): boto3 client connection

    Returns:
      (bool): dim_date file in processing bucket
    """
    logging.info("Checking for dim_date file in processing bucket")
    response = s3.list_objects_v2(Bucket="nc-terraformers-processing").get("Contents")
    if response:
        bucket_files = [file.get("Key") for file in response]
        for item in bucket_files:
            if item[: len("dim_date/dim_date")] == "dim_date/dim_date":
                logging.info(f"dim_date file found: {item}")
                return True
    logging.info("dim_date file not found")
    return False
