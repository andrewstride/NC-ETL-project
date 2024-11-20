
import pytest
import pandas as pd
from src.dim_date_table import dim_date

class TestDateTable:
    def test_dim_date_table_type(self):
        test = dim_date()
        assert isinstance(test, pd.DataFrame)

    def test_dim_date_table_length(self):
        test = dim_date()
        assert len(test) == 9497