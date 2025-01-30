from .agent import Agent

class Historian(Agent):
    def __init__(self, name="Dr. White"):
        super().__init__(name, expertise="History")