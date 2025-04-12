
# Multi-Agent Debate System with LLMs

This project implements a multi-agent debate system where LLM-based agents debate topics, fact-check arguments, and reach a consensus. It includes a Streamlit interface, a FastAPI endpoint, and SQLite storage for debate history.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Add API keys to `.env` (e.g., `OPENAI_API_KEY`, `PINECONE_API_KEY`)
3. Run the system:
   - Streamlit: `streamlit run src/app/interface.py`
   - FastAPI: `uvicorn src.app.api:app --reload`
4. Access debates at `http://localhost:8501` (Streamlit) or `http://localhost:8000/docs` (FastAPI).

## Features

- Specialized agents (Scientist, Economist, Ethicist, Historian)
- Robust fact-checking with multiple sources
- Dynamic debate flow with opening, rebuttal, and consensus phases
- Interactive Streamlit UI with visualizations
- Debate history stored in SQLite
- FastAPI endpoint for external integrations
