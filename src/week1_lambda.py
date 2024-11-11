from src.connection import db_connection
from src.utils import get_table

def lambda_handler(event, context):
    print(get_table("staff"))

# lambda_handler([],{})

    
