from src.utils.logger import Logger

class DebateFlow:
    def __init__(self, topic):
        self.topic = topic
        self.logger = Logger()

    def run_debate(self, agents, fact_checker, consensus):
        try:
            # Phase 1: Opening statements
            arguments = {}
            for agent in agents:
                argument = agent.generate_argument(self.topic)
                fact_check = fact_checker.check_fact(argument)
                arguments[agent.name] = {"text": argument, "fact_check": fact_check}
                self.logger.log(f"{agent.name} presents opening statement: {argument} ({fact_check['verdict']})")

            # Phase 2: Rebuttals
            rebuttals = []
            for agent in agents:
                for other_agent in agents:
                    if other_agent != agent:
                        response = other_agent.evaluate_argument(arguments[agent.name]["text"])
                        rebuttals.append({
                            "responder": other_agent.name,
                            "target": agent.name,
                            "response": response
                        })
                        self.logger.log(f"{other_agent.name} responds to {agent.name}: {response}")

            # Phase 3: Consensus
            consensus_text = consensus.reach_consensus([arg["text"] for arg in arguments.values()])
            self.logger.log(f"Consensus reached: {consensus_text}")

            return arguments, rebuttals, consensus_text
        except Exception as e:
            self.logger.log(f"Error running debate: {e}")
            return {}, [], "Error running debate."