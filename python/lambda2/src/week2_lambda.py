from src.convert_to_parquet_and_upload import (
    convert_to_parquet,
    upload_to_processing_bucket,
)
from src.dim_counterparty import dim_counterparty
from src.dim_currency import dim_currency
from src.dim_date_table import dim_date
from src.dim_design import dim_design
from src.dim_location import dim_location
from src.dim_staff import create_dim_staff
from src.fact_sales_order import fact_sales_order
from src.get_latest_file_as_df import get_latest_file_as_df
from src.utils import collate_csv_into_df

from datetime import datetime
import logging
import boto3

logger = logging.getLogger()
logger.setLevel("INFO")


def lambda_handler(event, context):
    """
    Event input:
    {"response": 200,
                "csv_files_written": {table_name : csv_file_written, table_name : csv_file_written},
                "timestamp_json_files_written": timestamp_json_files_written (list)}

    Returns:
    {"response": 200,
    "parquet_files_written": {table_name: parquet_files_written,
                                table_name2: pq file 2}
                                }
    """
    try:
        csv_files_written = event["csv_files_written"]
        # create s3 client
        s3 = boto3.client("s3")
        # create parquet_files_written dict
        parquet_files_written = {}
        # for table in parquet_files_written:
        for table in csv_files_written:
            match table:
                case "staff":
                    staff_df = get_latest_file_as_df(s3, csv_files_written[table])
                    dept_df = collate_csv_into_df(s3, "department")
                    dim_staff = create_dim_staff(staff_df, dept_df)
                    staff_pq = convert_to_parquet(dim_staff)
                    pq_written = upload_to_processing_bucket(s3, staff_pq, "dim_staff")
                case "design":
                    design_df = get_latest_file_as_df(s3, csv_files_written[table])
                    design_pq = convert_to_parquet(design_df)
                    pq_written = upload_to_processing_bucket(s3, design_pq, table)
                    parquet_files_written["dim_design"] = pq_written

        # match table name with util function & any other processes
        # staff and counterparty need to join on second table for transformation
        # if dim_date not in s3, write it
        # return output dict
        return {"response": 200, "parquet_files_written": parquet_files_written}

    except Exception as e:
        logging.error(e)


# TODO
# Put more CSV files in ingestion test bucket


# lambda
# lambda tests - MOCKING PATCHING
