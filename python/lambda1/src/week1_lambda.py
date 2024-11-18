from src.connection import db_connection
from src.utils import (
    get_all_rows,
    get_columns,
    write_to_s3,
    get_tables,
    fetch_last_timestamps_from_db,
    read_timestamp_from_s3,
    tables_and_timestamps_to_query,
    get_new_rows,
    write_df_to_csv,
    table_to_dataframe,
    timestamp_from_df,
    write_timestamp_to_s3,
)
from datetime import datetime
import json
import logging
import boto3

logger = logging.getLogger()


def lambda_handler(event, context):
    try:
        conn = db_connection()
        s3 = boto3.client("s3")
        for table in get_tables(conn):
            rows = get_all_rows(conn, table)
            columns = [get_columns(conn, table)]
            df = table_to_dataframe(rows, columns)
            write_df_to_csv(s3, df, table)
            write_timestamp_to_s3(s3, df, table)

            


            
        logger.error("Houston, we have a %s", "major problem", exc_info=True)
        return {"response": 200}

    except Exception as e:
        logging.error(e)
        return {"response": 500, "error": e}
