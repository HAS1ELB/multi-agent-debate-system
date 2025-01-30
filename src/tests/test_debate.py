from src.debate.debate_manager import DebateManager
from src.agents.scientist import Scientist

def test_debate_manager():
    scientist = Scientist()
    manager = DebateManager(agents=[scientist])
    manager.start_debate("Climate Change")