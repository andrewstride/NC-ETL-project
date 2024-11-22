import logging
import pandas as pd
from io import BytesIO
from pg8000.native import literal, identifier


def import_pq_to_df(s3, filename):
    """
    Gets Parquet file from s3 bucket and returns as Pandas Dataframe

    Parameters:
    s3: Boto3.client's3') connection
    Filename (str): filename to collect

    Returns:
    Pandas DataFrame"""
    try:
        logging.info(f"Reading {filename} from nc-terraformers-processing bucket")
        response = s3.get_object(Bucket="nc-terraformers-processing", Key=filename)
        body = response["Body"]
        pq = body.read()
        df = pd.read_parquet(BytesIO(pq))
        logging.info(f"{filename} file successfully imported into DataFrame")
        return df

    except Exception as e:
        logging.error(e)
        return {"result": "failure"}


def df_to_sql(df, table_name, conn):
    """
    Exports DataFrame into Data Warehouse table

    Parameters:
    df: Pandas DataFrame,
    table_name (str): name of table to export to,
    conn: PG8000 connection

    Returns:
    Number (int) of rows affected"""

    columns = list(df.columns)
    columns_str = ", ".join(f"{identifier(column)}" for column in columns)
    rows = list(df.values)
    if len(columns) == 0 or len(rows) == 0:
        logging.error(f"Malformed DataFrame: {df}")
        return None
    values_list = []
    for row in rows:
        values = [literal(v) for v in row]
        row_str = ", ".join(values)
        values_list.append(f"({row_str})")
    values_str = ", ".join(values_list)
    query = f"""INSERT INTO {identifier(table_name)}
            ({columns_str})
            VALUES {values_str} 
            RETURNING *;"""
    logging.info(f"Inserting values into {table_name}")
    try:
        result = conn.run(query)
        logging.info(f"{len(result)} rows inserted into {table_name} successfully")
        return len(result)
    except Exception as e:
        logging.error(e)
