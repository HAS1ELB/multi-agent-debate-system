from src.debate.debate_manager import DebateManager
from src.agents.scientist import Scientist

def test_debate_manager():
    scientist = Scientist()
    manager = DebateManager(agents=[scientist])
    arguments, rebuttals, consensus = manager.start_debate("Climate Change")
    assert arguments, "Arguments should not be empty"
    assert consensus, "Consensus should not be empty"