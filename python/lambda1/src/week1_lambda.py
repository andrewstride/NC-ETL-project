from src.connection import db_connection
from src.utils import get_rows, get_columns, write_to_s3
import logging
import boto3
import json

logger = logging.getLogger()

def lambda_handler(event, context):
    try:
        conn = db_connection()
        rows = get_rows(conn, "staff")
        columns = get_columns(conn, "staff")
        logger.error("Houston, we have a %s", "major problem", exc_info=True)
        staff_table = json.dumps(columns.append(rows))
        s3 = boto3.resource('s3')
        response = write_to_s3(s3, 'nc-terraformers-ingestion', 'staff', 'csv', staff_table)
        return {'response': 200,
                'body': response}
    except Exception as e:
        logging.error(e)
        return {'response': 500,
                'error': e}

