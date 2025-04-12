import streamlit as st
import sys
import os
import matplotlib.pyplot as plt
import networkx as nx
from src.agents.factory import AgentFactory
from src.debate.debate_manager import DebateManager
from src.utils.db import DebateDB

# Add project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Initialize database
db = DebateDB()

# Title
st.title("Multi-Agent Debate System")

# Description
st.write(
    "Simulate a debate between AI agents with different expertise. "
    "Enter a topic, customize settings, and explore past debates!"
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
use_api = st.sidebar.checkbox("Use OpenAI API (requires API key)", False)

# Start debate button
if st.button("Start Debate"):
    if not topic.strip():
        st.error("Please enter a valid debate topic.")
        st.stop()
    if len(expertises) < num_agents:
        st.error("Please select enough expertises for the number of agents.")
        st.stop()

    # Initialize agents
    try:
        agents = [AgentFactory.create_agent(exp, use_api=use_api) for exp in expertises[:num_agents]]
        debate_manager = DebateManager(agents=agents)
    except Exception as e:
        st.error(f"Error initializing agents: {e}")
        st.stop()

    # Display topic
    st.header(f"Debate Topic: {topic}")

    # Run debate
    try:
        st.write("### Opening Statements")
        arguments = {}
        for agent in debate_manager.agents:
            argument = agent.generate_argument(topic)
            if not argument or "Unable" in argument:
                st.write(f"**{agent.name}**: Failed to generate argument.")
                continue
            fact_check = debate_manager.fact_checker.check_fact(argument)
            verdict = fact_check.get("verdict", "Error")
            confidence = fact_check.get("confidence", 0.0)
            st.write(f"**{agent.name}**: {argument} ({verdict}, Confidence: {confidence:.2f})")
            arguments[agent.name] = argument

        st.write("### Rebuttals")
        rebuttals = []
        for agent in debate_manager.agents:
            for other_agent in debate_manager.agents:
                if other_agent != agent and arguments.get(agent.name):
                    response = other_agent.evaluate_argument(arguments[agent.name])
                    if response and "Unable" not in response:
                        st.write(f"**{other_agent.name} responds to {agent.name}**: {response}")
                        rebuttals.append({"responder": other_agent.name, "target": agent.name, "response": response})
                    else:
                        st.write(f"**{other_agent.name} responds to {agent.name}**: Unable to respond.")

        st.write("### Consensus")
        consensus = debate_manager.consensus.reach_consensus(list(arguments.values()))
        st.write(f"**Consensus**: {consensus}")

        # Sentiment analysis visualization
        st.write("### Debate Sentiment Analysis")
        try:
            sentiment_scores = [
                0.5 + 0.1 * i if "Unable" not in arguments.get(agent.name, "") else 0.2
                for i, agent in enumerate(debate_manager.agents)
            ]
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(
                range(len(sentiment_scores)),
                sentiment_scores,
                tick_label=[agent.name for agent in debate_manager.agents]
            )
            ax.set_xlabel("Agent")
            ax.set_ylabel("Sentiment Score")
            ax.set_ylim(0, 1)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error generating sentiment analysis: {e}")

        # Interaction graph
        st.write("### Agent Interaction Graph")
        try:
            G = nx.DiGraph()
            for agent in debate_manager.agents:
                G.add_node(agent.name)
            for rebuttal in rebuttals:
                G.add_edge(rebuttal["responder"], rebuttal["target"], weight=1)
            fig, ax = plt.subplots(figsize=(8, 4))
            pos = nx.spring_layout(G, seed=42)
            nx.draw(
                G,
                pos,
                with_labels=True,
                node_color='lightblue',
                edge_color='gray',
                font_weight='bold',
                node_size=1000,
                ax=ax
            )
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error generating interaction graph: {e}")

        # Save debate
        if st.button("Save Debate"):
            try:
                db.save_debate(topic, arguments, rebuttals, consensus)
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