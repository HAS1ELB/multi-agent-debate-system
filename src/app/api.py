from fastapi import FastAPI
from pydantic import BaseModel
from src.agents.factory import AgentFactory
from src.debate.debate_manager import DebateManager

app = FastAPI()

class DebateRequest(BaseModel):
    topic: str
    expertises: list[str]
    use_api: bool = False

@app.post("/debate")
async def start_debate(request: DebateRequest):
    agents = [AgentFactory.create_agent(exp, use_api=request.use_api) for exp in request.expertises]
    debate_manager = DebateManager(agents=agents)
    arguments, rebuttals, consensus = debate_manager.start_debate(request.topic)
    return {
        "topic": request.topic,
        "arguments": arguments,
        "rebuttals": rebuttals,
        "consensus": consensus
    }