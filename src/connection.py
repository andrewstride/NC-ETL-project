from pg8000.native import Connection
from dotenv import load_dotenv
import os

def db_connection():
    load_dotenv()
    conn = Connection(os.environ['PG_USER'], database=os.environ['PG_DATABASE'], password=os.environ['PG_PASSWORD'], host=os.environ['PG_HOST'], port=os.environ['PG_PORT'])
    return conn
    