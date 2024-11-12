from src.week1_lambda import lambda_handler
from src.utils import get_rows, get_columns
from src.connection import db_connection
from test_data import staff_table
import pytest
from unittest.mock import patch

# @pytest.fixture()
# def mock_connection():
#     mock_conn = Mock()
#     mock_conn.return_value = "return"
#     mock_conn.run('SELECT * FROM staff;')

class TestGetRows:
    def test_returns_list(self):
        conn = db_connection()
        assert isinstance(get_rows(conn, "staff"), list)

    def test_contains_lists(self):
        conn = db_connection()
        result = get_rows(conn, "staff")
        for row in result:
            assert isinstance(row, list)

    def test_correct_no_of_columns(self):
        conn = db_connection()
        result = get_rows(conn, "staff")
        for row in result:
            assert len(row) == 7

class TestGetColumns:
    def test_returns_list(self):
        conn = db_connection()
        assert isinstance(get_columns(conn, "staff"), list)

    def test_correct_no_of_columns(self):
        conn = db_connection()
        result = get_columns(conn, "staff")
        assert len(result) == 7