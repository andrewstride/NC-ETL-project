from src.connection import db_connection
from src.utils import (
    get_all_rows,
    get_columns,
    write_to_s3,
    get_tables,
    fetch_last_timestamps_from_db,
    get_new_rows,
)
from datetime import datetime
import json
import logging
import boto3

logger = logging.getLogger()


def lambda_handler(event, context):
    try:
        conn = db_connection()
        s3 = boto3.resource("s3")
        timestamp_dict = json.dumps(fetch_last_timestamps_from_db(conn))
        write_to_s3(
            s3, "nc-terraformers-ingestion", "timestamp_table", "json", timestamp_dict
        )
        for table in get_tables(conn):
            rows = get_all_rows(conn, table)
            columns_and_rows = [get_columns(conn, table)]
            for row in rows:
                columns_and_rows.append(row)
            timestamp = str(datetime.now())
            filename = f"{table}/{table}_{timestamp}"
            data = str(columns_and_rows)
            write_to_s3(s3, "nc-terraformers-ingestion", filename, "csv", data)
        logger.error("Houston, we have a %s", "major problem", exc_info=True)
        return {"response": 200}

    except Exception as e:
        logging.error(e)
        return {"response": 500, "error": e}
