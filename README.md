# Multi-Agent Debate System

This project is a **Multi-Agent Debate System** powered by Microsoft's **Autogen** framework. It simulates debates between AI agents with distinct expertises (Science, Economics, Ethics, History) to explore complex topics, fact-check arguments, and reach a consensus.

## Features

- **Autogen Orchestration**: Uses `AssistantAgent` and `RoundRobinGroupChat` for structured, asynchronous debates.
- **Specialized Agents**: Agents are prompted with specific expert personas (e.g., "Science Expert" focuses on empirical data).
- **Tool Integration**: Agents can autonomously use tools:
  - **Wikipedia Search**: Retrieves real-time context and summaries.
  - **Fact Checker**: Verifies claims using a retrieval-based pipeline.
- **Interactive UI**: A Streamlit-based interface that displays the debate in real-time, including tool usage and internal thought processes.
- **Model Flexibility**: Configured to use **OpenRouter** or **Groq** (e.g., Llama 3, Grok) via the OpenAI-compatible API.

## Architecture

The project has been migrated to a modern Autogen architecture:

- `src/agents/autogen_factory.py`: Creates agents with specific system messages and tools.
- `src/debate/autogen_manager.py`: Manages the debate flow using Autogen's group chat.
- `src/utils/autogen_tools.py`: Wraps Wikipedia and Fact Checking as callable tools.
- `src/app/interface.py`: The Streamlit frontend.

## Setup

1.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

    _Note: Some Autogen dependencies are installed in a local `libs` directory included in the project._

2.  **Configure Environment**:
    Create a `.env` file in the root directory and add your API key:

    ```env
    OPENROUTER_API_KEY=your_api_key_here
    # OR
    GROQ_API_KEY=your_api_key_here
    ```

3.  **Run the Application**:

    ```bash
    streamlit run src/app/interface.py
    ```

4.  **Usage**:
    - Open the app in your browser (usually `http://localhost:8501`).
    - Enter a topic (e.g., "Universal Basic Income").
    - Select the experts you want to debate.
    - Click **Start Debate** and watch them research and argue!

## Project Structure

```
src/
├── agents/             # Agent creation and configuration
├── app/                # Streamlit UI
├── debate/             # Debate management logic
├── fact_checking/      # Fact checking logic
├── knowledge/          # Data sources (Wikipedia)
└── utils/              # Utilities (Config, Logging)
```
