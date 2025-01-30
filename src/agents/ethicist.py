from .agent import Agent

class Ethicist(Agent):
    def __init__(self, name="Dr. Brown"):
        super().__init__(name, expertise="Ethics")