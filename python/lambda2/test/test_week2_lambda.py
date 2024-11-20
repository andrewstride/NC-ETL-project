import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.utils import dim_staff

class TestBucket:
    @patch("src.utils.dim_staff")
    def test_dim_staff_function_mock(self, mock_dim_staff):
        mock_dim_staff.return_value = "called the mock"
        mock_s3 = Mock()
        result = mock_dim_staff(mock_s3)
        mock_dim_staff.assert_called_once()
        assert result == "called the mock"
    

