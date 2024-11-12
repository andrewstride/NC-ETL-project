import pg8000
import os

def connect_to_db():
    # Fetch credentials from environment variables
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')
    port = int(os.environ.get('DB_PORT'))  # Ensure port is an integer
    database = os.environ.get('DB_NAME')

    # Establish the connection using pg8000
    connection = pg8000.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )
    return connection

# def test_db_connection():
#     conn = connect_to_db()
#     assert conn is not None  # Simple test to ensure connection is established
#     # You can add more assertions or test logic here as needed

def test_db_connection():
    conn = connect_to_db()
    if conn is None:
        raise Exception("Database connection failed")
    print("Database connection established successfully.")
