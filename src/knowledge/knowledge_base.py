from src.utils.logger import Logger

class KnowledgeBase:
    def __init__(self):
        self.logger = Logger()

    def query(self, question):
        try:
            return f"Answer: {question}"
        except Exception as e:
            self.logger.log(f"Error querying knowledge base: {e}")
            return "Error querying knowledge base."