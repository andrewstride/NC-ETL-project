import os
import pg8000 
import pytest

def test_database_connection():
    """Test that the database can be connected using the given URL."""
    database_url = os.getenv("DATABASE_URL")
    assert database_url, "DATABASE_URL is not set."

    try:
        # Establish a connection using the DATABASE_URL environment variable
        conn = pg8000.connect(database_url)
        conn.close()  # Connection successful if this line is reached
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")
