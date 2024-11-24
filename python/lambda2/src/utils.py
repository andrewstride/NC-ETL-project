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
