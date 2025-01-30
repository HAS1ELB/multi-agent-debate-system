from .agent import Agent

class Economist(Agent):
    def __init__(self, name="Dr. Jones"):
        super().__init__(name, expertise="Economics")