from .scientist import Scientist
from .economist import Economist
from .ethicist import Ethicist
from .historian import Historian
from .agent import Agent

class AgentFactory:
    @staticmethod
    def create_agent(expertise, name=None, use_api=False):
        if expertise == "Science":
            return Scientist(name or f"Dr. {expertise}", use_api=use_api)
        elif expertise == "Economics":
            return Economist(name or f"Dr. {expertise}", use_api=use_api)
        elif expertise == "Ethics":
            return Ethicist(name or f"Dr. {expertise}", use_api=use_api)
        elif expertise == "History":
            return Historian(name or f"Dr. {expertise}", use_api=use_api)
        else:
            return Agent(name or f"Dr. {expertise}", expertise=expertise, use_api=use_api)