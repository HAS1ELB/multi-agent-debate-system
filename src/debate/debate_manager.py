import streamlit as st
from src.debate.debate_flow import DebateFlow
from src.debate.consensus import Consensus
from src.fact_checking.fact_checker import FactChecker
from src.utils.logger import Logger

class DebateManager:
    def __init__(self, agents):
        self.agents = agents
        self.debate_flow = DebateFlow(topic="")
        self.fact_checker = FactChecker()
        self.consensus = Consensus()
        self.logger = Logger()

    def start_debate(self, topic):
        try:
            self.debate_flow.topic = topic
            arguments, rebuttals, consensus = self.debate_flow.run_debate(
                self.agents, self.fact_checker, self.consensus
            )
            return arguments, rebuttals, consensus
        except Exception as e:
            self.logger.log(f"Error starting debate: {e}")
            return {}, [], "Error starting debate."