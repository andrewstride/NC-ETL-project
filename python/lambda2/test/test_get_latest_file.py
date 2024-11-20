from src.get_latest_file import get_latest_file
from src.dim_design import dim_design
from testconf import processing_bucket, ingestion_bucket
from unittest.mock import patch
from testfixtures import LogCapture
import pandas as pd
import pytest

class TestGetLatestFile:
    def test_returns_a_dataframe(self,
                                 ingestion_bucket,
                                 processing_bucket):
        table_name = "design"
        response = get_latest_file(ingestion_bucket, table_name)
        assert isinstance(response, pd.DataFrame)

    def test_retreives_latest_data_from_given_table(self,
                                                    ingestion_bucket):
        table_name = "design"
        response = get_latest_file(ingestion_bucket, table_name)
        
        assert list(response.columns) == ["design_id",
                                          "created_at",
                                          "design_name",
                                          "file_location",
                                          "file_name",
                                          "last_updated"
                                        ]
        assert list(response.iloc[0]) == [1,
                                    "2024-11-03 14:20:49.962",
                                    "Steel",
                                    "/private",
                                    "steel-20220717-npgz.json",
                                    "2024-11-03 14:20:49.962"]
        
    def test_function_handles_error(self):
        fake_bucket = ""
        table_name = ""
        with LogCapture() as l:
            output = get_latest_file(ingestion_bucket, table_name)
            assert output == {"result": "Failure"}
            assert "ERROR" in str(l)

    def test_function_filters_by_given_table(self,
                                             ingestion_bucket,
                                             processing_bucket):
        table_name = "staff"
        response = get_latest_file(ingestion_bucket, table_name)
        
        assert list(response.columns) == ["staff_id",
                                          "created_at",
                                          "staff_name",
                                          "file_location",
                                          "file_name",
                                          "last_updated"
                                        ]

        assert list(response.iloc[0]) == [100,
                                    "2000-11-03 14:20:49.962",
                                    'Brick',
                                    '/private',
                                    'brick-20220717-npgz.json',
                                    "2000-11-03 14:20:49.962"]