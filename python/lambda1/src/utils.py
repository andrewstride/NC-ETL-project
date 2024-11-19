from pg8000.exceptions import DatabaseError
from botocore.exceptions import ClientError, ParamValidationError
import botocore
from pg8000.native import identifier
import logging
import json
import pandas as pd
from io import StringIO
from datetime import datetime


def get_tables(conn):
    data = conn.run(
        """ SELECT table_name 
             FROM information_schema.tables 
             WHERE table_schema='public' 
             AND table_type='BASE TABLE';"""
    )
    tables_list = [item[0] for item in data if item[0] != "_prisma_migrations"]
    return tables_list


def get_all_rows(conn, table):
    """Returns rows from table

    Parameters:
        Connection: PG8000 Connection to database,
        Table (str): Table name to access in database


    Returns:
        List (list): The lists are rows from table
    """
    if table in get_tables(conn):
        data = conn.run(f"SELECT * FROM {identifier(table)};")
        return data
    else:
        logging.error("Table not found")
        return ["Table not found"]


def get_columns(conn, table):
    """Returns columns from table

    Parameters:
        Connection: PG8000 Connection to database,
        Table (str): Table name to access in database


    Returns:
        List (list): A list of columns
    """
    if table in get_tables(conn):
        conn.run(f"SELECT * FROM {identifier(table)};")
        columns = [col["name"] for col in conn.columns]
        return columns
    else:
        logging.error("Table not found")
        return ["Table not found"]


def write_to_s3(s3, bucket_name, filename, format, data):
    """Writes to s3 bucket

     Parameters:
        s3: Boto3.client's3') connection,
        Bucket Name (str): Bucket name to write to
        Filename (str): Filename to write
        Format (str): Format to write
        Data (json): JSON of data to write

    Returns:
        Dict (dict): {"result": "Failure/Success"}
    """
    try:
        s3.put_object(Bucket=bucket_name, Key=f"{filename}.{format}", Body=data)
    except (ClientError, ParamValidationError) as e:
        logging.error(e)
        return {"result": "Failure"}
    return {"result": "Success"}


def read_timestamp_from_s3(s3, table):
    """Reads timestamp of given table from s3 ingestion bucket

    Parameters:
        s3: Boto3.client('s3') connection
        Table Name (str)

    Returns:
        Dictionary of format {'Table Name':'Timestamp String'}
    """
    try:
        filename = f"{table}_timestamp.json"
        response = s3.get_object(Bucket="nc-terraformers-ingestion", Key=filename)
        body = response["Body"]
        return json.loads(body.read().decode())
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return {"detail": "No timestamp exists"}
        logging.error(e)
        return {"result": "Failure"}


def get_new_rows(conn, table, timestamp):
    """Returns rows from table

    Parameters:
        Connection: PG8000 Connection to database,
        Table (str): Table name to access in database
        Timestamp (str): format 'YYYY-MM-DD HH24:MI:SS.US'

    Returns:
        List (list): The lists are rows from table
    """
    try:
        if table in get_tables(conn):
            data = conn.run(
                f"""SELECT * FROM {identifier(table)}
                            WHERE last_updated > to_timestamp(:timestamp,
                            'YYYY-MM-DD HH24:MI:SS.US');""",
                timestamp=timestamp,
            )
            return data
        else:
            logging.error("Table not found")
    except Exception as e:
        logging.error(e)
    return []


def write_df_to_csv(s3, df, table_name):
    """Takes rows, columns, and name of a table, converts it
    to csv file format, and uploads the file to s3 Ingestion bucket.

    Paramaters:
        s3: Boto3.client('s3') connection
        Rows (list of lists): the rows of the table
        Columns (list): the columns of the table
        Table_name (str): the name of the table

    Returns:
        Dict (dict): {"result": "Failure/Success"} + "detail" if successful.
    """
    timestamp = str(datetime.now())
    try:
        with StringIO() as csv:
            df.to_csv(csv, index=False)
            data = csv.getvalue()
            response = write_to_s3(
                s3,
                "nc-terraformers-ingestion",
                f"{table_name}/{table_name}_{timestamp}",
                "csv",
                data,
            )
            if response["result"] == "Success":
                return {
                    "result": "Success",
                    "detail": "Converted to csv, uploaded to ingestion bucket",
                }
    except Exception as e:
        logging.error(e)
    return {"result": "Failure"}


def table_to_dataframe(rows, columns):
    try:
        return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        logging.error(e)


def timestamp_from_df(df):
    try:
        return df["last_updated"].max()
    except KeyError as e:
        logging.error({"column not found": e})


def write_timestamp_to_s3(s3, df, table):
    try:
        timestamp_json = json.dumps({table: str(timestamp_from_df(df))})
        filename = f"{table}_timestamp"
        write_to_s3(s3, "nc-terraformers-ingestion", filename, "json", timestamp_json)
        return {"result": "Success"}
    except Exception as e:
        logging.error(e)
        return {"result": "Failure"}
