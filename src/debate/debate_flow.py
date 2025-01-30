class DebateFlow:
    def __init__(self, topic):
        self.topic = topic

    def opening_statements(self, agents):
        for agent in agents:
            print(f"{agent.name} presents their opening statement.")