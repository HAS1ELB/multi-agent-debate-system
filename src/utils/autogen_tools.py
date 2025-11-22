from src.knowledge.data_sources.wikipedia import Wikipedia
from src.fact_checking.fact_checker import FactChecker
from typing import Annotated

# Initialize instances globally to avoid overhead on every call
_wikipedia = Wikipedia()
_fact_checker = FactChecker()

def search_wikipedia(query: Annotated[str, "The topic or query to search on Wikipedia"]) -> str:
    """
    Searches Wikipedia for the given query and returns a summary.
    Use this to gather factual context about a debate topic.
    """
    return _wikipedia.search(query)

def check_fact(claim: Annotated[str, "The statement or claim to verify"]) -> str:
    """
    Verifies a factual claim using the fact checker.
    Returns a verdict (True/False/Uncertain), confidence score, and context.
    """
    result = _fact_checker.check_fact(claim)
    return f"Verdict: {result['verdict']}, Confidence: {result['confidence']:.2f}, Context: {result['context']}"
