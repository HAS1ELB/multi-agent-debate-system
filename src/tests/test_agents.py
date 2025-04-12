from src.agents.scientist import Scientist
from src.agents.economist import Economist

def test_scientist_argument():
    scientist = Scientist()
    argument = scientist.generate_argument("Climate Change")
    assert argument is not None, "Argument should not be None"
    assert len(argument.split()) > 50, "Argument too short"
    assert "climate" in argument.lower(), "Topic not mentioned"

def test_economist_argument():
    economist = Economist()
    argument = economist.generate_argument("Climate Change")
    assert argument is not None, "Argument should not be None"
    assert len(argument.split()) > 50, "Argument too short"
    assert "economic" in argument.lower() or "cost" in argument.lower(), "Economic focus missing"