import sys
import os

# Ajoutez le répertoire racine du projet au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.agents.scientist import Scientist
from src.agents.economist import Economist
from src.debate.debate_manager import DebateManager

def main():
    scientist = Scientist()
    economist = Economist()
    debate_manager = DebateManager(agents=[scientist, economist])
    debate_manager.start_debate(topic="Climate Change")

if __name__ == "__main__":
    main()