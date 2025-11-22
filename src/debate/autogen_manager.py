import asyncio
import re
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from src.agents.autogen_factory import AutogenAgentFactory

class AutogenDebateManager:
    def __init__(self, expertises):
        self.agents = []
        for exp in expertises:
            # Sanitize name to be a valid Python identifier
            sanitized_exp = re.sub(r'\W|^(?=\d)', '_', exp)
            agent_name = f"{sanitized_exp}_Expert"
            self.agents.append(AutogenAgentFactory.create_agent(agent_name, exp))
        
        self.team = RoundRobinGroupChat(
            participants=self.agents,
            max_turns=len(self.agents) * 2  # 2 rounds per agent
        )

    async def run_debate(self, topic):
        """
        Runs the debate and yields messages as they are generated.
        """
        task = f"Let's debate the topic: '{topic}'. {self.agents[0].name}, please start with an opening statement."
        stream = self.team.run_stream(task=task)
        
        async for message in stream:
            # We are interested in TextMessage and potentially ToolCall/ToolOutput
            # For simplicity, we'll yield the string representation or specific fields
            yield message
