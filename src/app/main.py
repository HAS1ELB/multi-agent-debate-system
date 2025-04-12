import sys
import os
from src.agents.factory import AgentFactory
from src.debate.debate_manager import DebateManager

# Add project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def main():
    scientist = AgentFactory.create_agent("Science", use_api=False)
    economist = AgentFactory.create_agent("Economics", use_api=False)
    debate_manager = DebateManager(agents=[scientist, economist])
    debate_manager.start_debate(topic="Climate Change")

if __name__ == "__main__":
    main()