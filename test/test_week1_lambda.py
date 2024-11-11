from src.week1_lambda import lambda_handler
from src.utils import get_table
from src.connection import db_connection
import pytest
# from unittest.mock import patch

class TestGetTable:
    def test_returns_list(self):
        conn = db_connection()
        assert isinstance(get_table(conn, "staff"), list)

