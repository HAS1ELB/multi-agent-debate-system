from src.fact_checking.fact_checker import FactChecker

def test_fact_checker():
    checker = FactChecker()
    assert checker.check_fact("Test claim") is not None