from .agent import Agent

class Scientist(Agent):
    def __init__(self, name="Dr. Smith"):
        super().__init__(name, expertise="Science")