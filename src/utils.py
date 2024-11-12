from src.connection import db_connection
import pandas as pd


def get_rows(connection, table):
    '''
    Returns rows from table

    Parameters:
        Connection: PG8000 Connection to database,
        Table (str): Table name to access in database


    Returns:
        List (list): The lists are rows from table
    '''
    conn = connection
    query = "SELECT * FROM " + table + ";"
    data = conn.run(query)
    return data

def get_columns(connection, table):
    '''
    Returns columns from table

    Parameters:
        Connection: PG8000 Connection to database,
        Table (str): Table name to access in database


    Returns:
        List (list): A list of columns
    '''
    conn = connection
    query = "SELECT * FROM " + table + ";"
    conn.run(query)
    columns = [col['name'] for col in conn.columns]
    return columns