from src.connection import db_connection

def get_table(connection, table):
    conn = connection
    query = "SELECT * FROM " + table + ";"
    data = conn.run(query)
    return data