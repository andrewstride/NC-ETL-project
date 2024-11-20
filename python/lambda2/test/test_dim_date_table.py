import pytest
import pandas
from src.dim_date_table import dim_date

class TestDateTable:
    def test_dim_date_table_length(self):
        test = dim_date()
        assert len(test) == 9497
    
    def test_dim_date_table_type(self):
        test = dim_date()
        assert test != isnull
        print(dir(test))