import time
import streamlit as st

class DebateManager:
    def __init__(self, agents):
        self.agents = agents

    def start_debate(self, topic):
        for round in range(3):  # 3 tours de débat
            st.write(f"### Round {round + 1}")
            for agent in self.agents:
                argument = agent.generate_argument(topic)
                st.write(f"**{agent.name}**: {argument}")
                for other_agent in self.agents:
                    if other_agent != agent:
                        response = other_agent.evaluate_argument(argument)
                        st.write(f"**{other_agent.name} responds**: {response}")