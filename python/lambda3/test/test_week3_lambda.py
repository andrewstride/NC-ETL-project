from src.week3_lambda import lambda_handler

class TestDummy:
    def test_dummy_test(self):
        lambda_handler([],[])
        assert 1 == 1