from src.connection import db_connection
from src.utils import get_rows, get_columns

def lambda_handler(event, context):
    conn = db_connection()
    rows = get_rows(conn, "staff")
    columns = get_columns(conn, "staff")
    
# lambda_handler([],{})

    
