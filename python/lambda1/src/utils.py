from botocore.exceptions import ClientError, ParamValidationError
import logging


def get_tables(connection):
    conn = connection
    data = conn.run(""" SELECT table_name 
             FROM information_schema.tables 
             WHERE table_schema='public' 
             AND table_type='BASE TABLE';""")
    tables_list = [item[0] for item in data if item[0] != '_prisma_migrations']
    return tables_list

def get_rows(connection, table):
    '''Returns rows from table

    Parameters:
        Connection: PG8000 Connection to database,
        Table (str): Table name to access in database


    Returns:
        List (list): The lists are rows from table
    '''
    conn = connection
    if table in get_tables(conn):
        query = "SELECT * FROM " + table + ";"
        data = conn.run(query)
        return data
    else:
        logging.error("Table not found")
        return ['Table not found']

def get_columns(connection, table):
    '''Returns columns from table

    Parameters:
        Connection: PG8000 Connection to database,
        Table (str): Table name to access in database


    Returns:
        List (list): A list of columns
    '''
    conn = connection
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
