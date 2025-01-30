from src.agents.scientist import Scientist

def test_scientist():
    scientist = Scientist()
    assert scientist.generate_argument("Climate Change") is not None