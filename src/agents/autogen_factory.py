import os
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from src.utils.config import Config
from src.utils.autogen_tools import search_wikipedia, check_fact

class AutogenAgentFactory:
    @staticmethod
    def create_agent(name, expertise, model_client=None):
        if model_client is None:
            # Default to OpenRouter/Groq if not provided
            api_key = os.getenv("GROQ_API_KEY") or os.getenv("OPENROUTER_API_KEY")
            base_url = "https://api.groq.com/openai/v1" if os.getenv("GROQ_API_KEY") else "https://openrouter.ai/api/v1"
            model_name = "llama-3.3-70b-versatile" if os.getenv("GROQ_API_KEY") else "x-ai/grok-4.1-fast:free"
            
            model_client = OpenAIChatCompletionClient(
                model=model_name,
                api_key=api_key,
                base_url=base_url,
                model_capabilities={
                    "vision": False,
                    "function_calling": True,
                    "json_output": True,
                }
            )

        system_message = f"You are a {expertise} expert. "
        if expertise == "Science":
            system_message += "You rely on data, research, and empirical evidence. Focus on facts and scientific consensus."
        elif expertise == "Economics":
            system_message += "You focus on cost-benefit analysis, market trends, and economic impact."
        elif expertise == "Ethics":
            system_message += "You focus on moral principles, societal impact, and ethical implications."
        elif expertise == "History":
            system_message += "You focus on historical context, past precedents, and long-term trends."
        
        return AssistantAgent(
            name=name,
            system_message=system_message,
            model_client=model_client,
            tools=[search_wikipedia, check_fact]
        )
