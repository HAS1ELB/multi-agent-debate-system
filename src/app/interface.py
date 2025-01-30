import streamlit as st
import sys
import os

# Ajoutez le répertoire racine du projet au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import matplotlib.pyplot as plt
from src.agents.scientist import Scientist
from src.agents.economist import Economist
from src.agents.ethicist import Ethicist
from src.agents.historian import Historian
from src.debate.debate_manager import DebateManager

# Titre de l'application
st.title("Multi-Agent Debate System")

# Description de l'application
st.write(
    "This application allows you to simulate a debate between AI agents with different expertise. "
    "Enter a topic below and see how the agents discuss it!"
)

# Saisie du sujet de débat
topic = st.text_input("Enter a debate topic:", "Climate Change")

# Options de personnalisation
st.sidebar.header("Settings")
num_agents = st.sidebar.slider("Number of Agents", 2, 4, 2)
expertises = st.sidebar.multiselect(
    "Select Expertises",
    ["Science", "Economics", "Ethics", "History"],
    default=["Science", "Economics"]
)

# Bouton pour démarrer le débat
if st.button("Start Debate"):
    # Initialisation des agents en fonction des expertises sélectionnées
    agents = []
    for expertise in expertises:
        if expertise == "Science":
            agents.append(Scientist())
        elif expertise == "Economics":
            agents.append(Economist())
        elif expertise == "Ethics":
            agents.append(Ethicist())
        elif expertise == "History":
            agents.append(Historian())

    # Limiter le nombre d'agents en fonction de la sélection de l'utilisateur
    agents = agents[:num_agents]

    # Initialisation du gestionnaire de débat
    debate_manager = DebateManager(agents=agents)

    # Affichage du sujet
    st.header(f"Debate Topic: {topic}")

    # Démarrage du débat
    st.write("### Opening Statements")
    arguments = []
    for agent in debate_manager.agents:
        argument = agent.generate_argument(topic)
        st.write(f"**{agent.name}**: {argument}")
        arguments.append(argument)

    st.write("### Rebuttals")
    responses = []
    for agent in debate_manager.agents:
        for other_agent in debate_manager.agents:
            if other_agent != agent:
                response = other_agent.evaluate_argument(argument)
                st.write(f"**{other_agent.name} responds to {agent.name}**: {response}")
                responses.append(response)

    # Affichage des visuels (analyse de sentiment)
    st.write("### Debate Sentiment Analysis")
    try:
        # Générer des scores de sentiment dynamiques en fonction du nombre d'agents
        sentiment_scores = [0.5 + 0.1 * i for i in range(len(debate_manager.agents))]  # Exemple de scores de sentiment
        plt.bar(range(len(sentiment_scores)), sentiment_scores)
        plt.xlabel("Agent")
        plt.ylabel("Sentiment Score")
        plt.xticks(range(len(sentiment_scores)), [agent.name for agent in debate_manager.agents])
        st.pyplot(plt)
    except Exception as e:
        st.error(f"An error occurred while generating the sentiment analysis: {e}")

    # Sauvegarder les débats
    if st.button("Save Debate"):
        with open("data/debates/debate_log.txt", "w") as f:
            f.write(f"Debate Topic: {topic}\n")
            f.write("### Arguments:\n")
            for argument in arguments:
                f.write(f"- {argument}\n")
            f.write("### Responses:\n")
            for response in responses:
                f.write(f"- {response}\n")
        st.success("Debate saved successfully!")

# Informations supplémentaires
st.sidebar.header("About")
st.sidebar.write(
    "This project uses AI models to simulate a debate between agents with different expertise. "
    "The agents generate arguments and evaluate each other's points to reach a consensus."
)

st.sidebar.header("Instructions")
st.sidebar.write(
    "1. Enter a debate topic in the text box.\n"
    "2. Adjust the number of agents and their expertises in the sidebar.\n"
    "3. Click 'Start Debate' to see the agents discuss the topic.\n"
    "4. Save the debate to review it later."
)