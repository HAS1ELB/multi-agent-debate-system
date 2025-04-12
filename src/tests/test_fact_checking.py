from src.fact_checking.fact_checker import FactChecker

def test_fact_checker():
    checker = FactChecker()
    result = checker.check_fact("The Earth is round.")
    assert result["verdict"] in ["True", "False", "Uncertain"], "Invalid verdict"
    assert result["confidence"] >= 0.0, "Confidence should be non-negative"