from src.utils import get_rows, get_columns
import json
import boto3
import os
import psycopg2


# from src.connection import db_connection
# from src.utils import get_rows, get_columns

def lambda_handler(event, context):
    # Load credentials from AWS Secret Manager
    secret_name = os.environ["totesys-conn"]
    region_name = os.environ["eu-west-2"]

    secrets_client = boto3.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        # Retrieve database credentials from Secret Manager
        secret_value = secrets_client.get_secret_value(SecretId=secret_name)
        secret = json.loads(secret_value['SecretString'])

        db_host = secret['pg_host']
        db_user = secret['pg_user']
        db_password = secret['pg_password']
        db_name = secret['pg_database']

        # Establish connection to the database
        connection = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            dbname=db_name
        )

        cursor = connection.cursor()

        # Querying connected database - NEEDS MORE WORK
        query = ([content for content in zip(get_columns,get_rows)])
        cursor.execute(query)

        # Fetch data - NEEDS MORE WORK
        results = cursor.fetchall()

        # Close connection
        cursor.close()
        connection.close()

        return {
            'statusCode': 200,
            'body': json.dumps(results)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(results)
        }


lambda_handler([],{})

    
