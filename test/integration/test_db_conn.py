# import pg8000
# import os

# def connect_to_db():
#     # Fetch credentials from environment variables
#     user = os.environ.get('DB_USER')
#     password = os.environ.get('DB_PASSWORD')
#     host = os.environ.get('DB_HOST')
#     port = os.environ.get('DB_PORT')  # Ensure port is an integer
#     database = os.environ.get('DB_NAME')

#     # Establish the connection using pg8000
#     connection = pg8000.connect(
#         user=user,
#         password=password,
#         host=host,
#         port=port,
#         database=database
#     )
#     return connection


# def test_db_connection():
#     conn = connect_to_db()
#     assert conn 
   