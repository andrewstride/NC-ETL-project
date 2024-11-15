from pg8000.exceptions import DatabaseError
from botocore.exceptions import ClientError, ParamValidationError
import logging
import json


def get_tables(conn):
    data = conn.run(""" SELECT table_name 
             FROM information_schema.tables 
             WHERE table_schema='public' 
             AND table_type='BASE TABLE';""")
    tables_list = [item[0] for item in data if item[0] != '_prisma_migrations']
    return tables_list

def get_all_rows(conn, table):
    '''Returns rows from table

    Parameters:
        Connection: PG8000 Connection to database,
        Table (str): Table name to access in database


    Returns:
        List (list): The lists are rows from table
    '''
    if table in get_tables(conn):
        query = "SELECT * FROM " + table + ";"
        data = conn.run(query)
        return data
    else:
        logging.error("Table not found")
        return ['Table not found']

def get_columns(conn, table):
    '''Returns columns from table

    Parameters:
        Connection: PG8000 Connection to database,
        Table (str): Table name to access in database


    Returns:
        List (list): A list of columns
    '''
    if table in get_tables(conn):
        query = "SELECT * FROM " + table + ";"
        conn.run(query)
        columns = [col['name'] for col in conn.columns]
        return columns
    else:
        logging.error("Table not found")
        return ['Table not found']

def write_to_s3(s3, bucket_name, filename, format, data):
    '''Writes to s3 bucket

     Parameters:
        s3: Boto3.resource('s3') connection,
        Bucket Name (str): Bucket name to write to
        Filename (str): Filename to write
        Format (str): Format to write
        Data (json): JSON of data to write

    Returns:
        Dict (dict): {"result": "Failure/Success"}
    '''
    try:
        s3_key = f"{filename}.{format}"
        object = s3.Object(bucket_name, s3_key)
        object.put(Body=data)
    except (ClientError, ParamValidationError) as e:
        logging.error(e)
        return {"result": "Failure"}
    return {"result": "Success"}

def fetch_last_timestamps_from_db(conn):
    '''Fetches latest timestamp from db

    Parameters: 
        Connection: PG8000 Connection to database

    Returns:
        Dictionary of {'Table Name': 'Timestamp string'}

    '''
    tables = get_tables(conn)
    output_dict = {}
    for table in tables:
        try:
            query = "SELECT max(last_updated) FROM " + table + ";"
            data = conn.run(query)
            output_dict[table] = f"{data[0][0]}"
        except DatabaseError as e:
            logging.error(e)
    return output_dict

def read_timestamps_table_from_s3(s3, bucket_name, filename):
    '''Reads file from given s3 bucket
    
    Parameters:
        s3: Boto3.client('s3') connection
        Bucket Name (str)
        File Name (str)

    Returns:
        Dictionary of format {'Table Name':'Timestamp String'}
    '''
    try:
        response = s3.get_object(Bucket=bucket_name, Key=filename)
        body = response['Body']
        return json.loads(body.read().decode())
    except ClientError as e:
        logging.error(e)
        return {"result": "Failure"}
    
def tables_and_timestamps_to_query(db_timestamps, s3_timestamps):
    '''Produces dictionary of tables to query and timestamps to query after
    
    Parameters:
        Timestamps from DB (dict): Timestamps table
        Timestamps from s3 (dict): Timestamps table
        
    Returns:
        returns a dict: {'table name':'timestamp from s3'} where timestamp differs
        '''
    output_dict = {}
    for table in db_timestamps:
        try:
            if s3_timestamps[table] != db_timestamps[table]:
                output_dict[table] = s3_timestamps[table]
        except KeyError as e:
            logging.error({'KeyError':str(e)})
    return output_dict

def get_new_rows(conn, table, timestamp):
    '''Returns rows from table

    Parameters:
        Connection: PG8000 Connection to database,
        Table (str): Table name to access in database
        Timestamp (str): format 'YYYY-MM-DD HH24:MI:SS.US'

    Returns:
        List (list): The lists are rows from table
    '''
    if table in get_tables(conn):
        query = "SELECT * FROM " + table + " WHERE last_updated > to_timestamp(:timestamp, 'YYYY-MM-DD HH24:MI:SS.US');"
        data = conn.run(query, timestamp=timestamp)
        return data
    else:
        logging.error("Table not found")
        return ['Table not found']



# func: read s3 data and reupload with new data added

def reformat_data(conn, rows, columns, table_name):
    '''Takes rows, columns, and name of a table, converts it
    to csv file format, and uploads the file to s3 Ingestion bucket.

    Paramaters: 
        s3: Boto3.client('s3') connection
        Rows (list): the rows of the table
        Columns (list of lists): the columns of the table
        Table_name (str): the name of the table

    Returns:
        A message (str) saying whether the upload was successful.
    
    '''
    pass


# write latest timestamps to timestamp table


# Change file structure to match main branch before merge

# pg8000.native import identifier