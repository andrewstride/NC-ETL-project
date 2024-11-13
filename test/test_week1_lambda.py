from src.week1_lambda import lambda_handler
from src.utils import get_rows, get_columns
from src.connection import db_connection, get_db_creds
import logging
from testfixtures import LogCapture


class TestGetDBCreds:
    def test_correct_keys_in_dict(self):
        creds = get_db_creds()
        keys = list(creds.keys())
        assert 'username' in keys
        assert 'password' in keys
        assert 'host' in keys
        assert 'port' in keys
        assert 'dbname' in keys

    def test_values_are_strings(self):
        creds = get_db_creds()
        for cred in creds:
            assert isinstance(creds[cred], str)

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

class TestLogger:
    def test_token_logger(self):
        with LogCapture() as l:
            lambda_handler([],{})
            l.check_present(('root', 'ERROR', 'Houston, we have a major problem'))

           
