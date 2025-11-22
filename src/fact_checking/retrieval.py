import wikipedia
from src.utils.logger import Logger

class Retrieval:
    def __init__(self):
        wikipedia.set_lang('en')
        self.logger = Logger()

    def retrieve(self, query):
        try:
            # Search for the query
            search_results = wikipedia.search(query)
            if not search_results:
                return "No information found."

            # Try to get the summary of the first result
            try:
                return wikipedia.summary(search_results[0], auto_suggest=False)
            except wikipedia.DisambiguationError as e:
                return wikipedia.summary(e.options[0], auto_suggest=False)
            except wikipedia.PageError:
                if len(search_results) > 1:
                    return wikipedia.summary(search_results[1], auto_suggest=False)
                else:
                    return "No information found."
        except Exception as e:
            self.logger.log(f"Error retrieving data for {query}: {e}")
            return "Error retrieving information."