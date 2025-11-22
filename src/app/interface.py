import streamlit as st
import sys
import os
import asyncio
import matplotlib.pyplot as plt
import networkx as nx

# Add project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# Add libs to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "libs"))

from src.debate.autogen_manager import AutogenDebateManager
from src.utils.db import DebateDB
from autogen_agentchat.messages import TextMessage, ToolCallRequestEvent, ToolCallExecutionEvent, ToolCallSummaryMessage

# Initialize database
db = DebateDB()

# Title
st.title("Multi-Agent Debate System (Autogen)")

# Description
st.write(
    "Simulate a debate between AI agents with different expertise using Microsoft Autogen. "
    "Enter a topic, customize settings, and watch the debate unfold!"
)

# Debate topic input
topic = st.text_input("Enter a debate topic:", "Climate Change")

# Sidebar settings
st.sidebar.header("Settings")
num_agents = st.sidebar.slider("Number of Agents", 2, 4, 2)
expertises = st.sidebar.multiselect(
    "Select Expertises",
    ["Science", "Economics", "Ethics", "History"],
    default=["Science", "Economics"]
)

# Start debate button
if st.button("Start Debate"):
    if not topic.strip():
        st.error("Please enter a valid debate topic.")
        st.stop()
    if len(expertises) < num_agents:
        st.error("Please select enough expertises for the number of agents.")
        st.stop()

    # Initialize manager
    try:
        debate_manager = AutogenDebateManager(expertises=expertises[:num_agents])
    except Exception as e:
        st.error(f"Error initializing Autogen manager: {e}")
        st.stop()

    # Display topic
    st.header(f"Debate Topic: {topic}")

    # Run debate
    async def run_debate_ui():
        st.write("### Debate in Progress...")
        container = st.container()
        arguments = []
        
        async for message in debate_manager.run_debate(topic):
            # Display message
            with container:
                # Handle TextMessage
                if isinstance(message, TextMessage):
                    st.markdown(f"**{message.source}**: {message.content}")
                    arguments.append(f"{message.source}: {message.content}")
                
                # Handle Tool Calls (optional: show as expander or status)
                elif isinstance(message, ToolCallRequestEvent):
                    with st.expander(f"🛠️ {message.source} using tools..."):
                        for tool_call in message.content:
                            st.write(f"Calling: `{tool_call.name}` with `{tool_call.arguments}`")
                
                # Handle Tool Outputs
                elif isinstance(message, ToolCallExecutionEvent):
                    with st.expander(f"✅ Tool Output for {message.source}", expanded=False):
                        for result in message.content:
                            st.write(f"Result: {result.content[:200]}...") # Truncate for readability

                # Handle Summary
                elif isinstance(message, ToolCallSummaryMessage):
                     st.info(f"**{message.source}** (Tool Summary): {message.content}")
                
                # Ignore other types (like GroupChatTermination) to avoid raw dumps
                else:
                    # Uncomment for debugging
                    # st.write(f"Debug: {type(message)} - {message}")
                    pass

        return arguments

    try:
        # Run the async debate
        arguments = asyncio.run(run_debate_ui())
        
        # Save debate
        if st.button("Save Debate"):
            try:
                # Simplified save for now
                db.save_debate(topic, {"log": arguments}, [], "See log")
                st.success("Debate saved successfully!")
            except Exception as e:
                st.error(f"Error saving debate: {e}")

    except Exception as e:
        st.error(f"Error running debate: {e}")

# Debate history
st.sidebar.header("Debate History")
if st.sidebar.button("View Past Debates"):
    try:
        debates = db.get_debates()
        if debates:
            for debate in debates:
                with st.expander(f"Debate on {debate['topic']} ({debate['date']})"):
                    st.write(f"**Arguments**: {debate['arguments']}")
                    st.write(f"**Rebuttals**: {debate['rebuttals']}")
                    st.write(f"**Consensus**: {debate['consensus']}")
        else:
            st.write("No past debates found.")
    except Exception as e:
        st.error(f"Error retrieving debates: {e}")

# About
st.sidebar.header("About")
st.sidebar.write(
    "This project uses AI models to simulate debates between agents with different expertise. "
    "It supports fact-checking, visualizations, and debate history storage."
)

# Instructions
st.sidebar.header("Instructions")
st.sidebar.write(
    "1. Enter a debate topic.\n"
    "2. Adjust agents and expertise in the sidebar.\n"
    "3. Click 'Start Debate' to begin.\n"
    "4. Save debates and view history."
)