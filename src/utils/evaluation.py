from src.utils.logger import Logger

class Evaluation:
    def __init__(self):
        self.logger = Logger()

    def evaluate(self, debate):
        try:
            return "Debate evaluated."
        except Exception as e:
            self.logger.log(f"Error evaluating debate: {e}")
            return "Error evaluating debate."