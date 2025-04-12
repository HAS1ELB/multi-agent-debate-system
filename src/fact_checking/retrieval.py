import wikipediaapi
from src.utils.logger import Logger

class Retrieval:
    def __init__(self):
        self.wiki_wiki = wikipediaapi.Wikipedia(
            language='en',
            user_agent='MultiAgentDebateSystem/1.0'
        )
        self.logger = Logger()

    def retrieve(self, query):
        try:
            page = self.wiki_wiki.page(query)
            return page.summary if page.exists() else "No information found."
        except Exception as e:
            self.logger.log(f"Error retrieving data for {query}: {e}")
            return "Error retrieving information."