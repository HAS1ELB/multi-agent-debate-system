import wikipedia
from src.utils.logger import Logger
from src.utils.cache import cache

class Wikipedia:
    def __init__(self, language='en'):
        wikipedia.set_lang(language)
        self.logger = Logger()

    def search(self, query):
        cache_key = f"wiki_{query}"
        if cache_key in cache:
            return cache[cache_key]

        try:
            # First, search for the query to get relevant page titles
            search_results = wikipedia.search(query)
            if not search_results:
                return "No information found."

            # Try to get the summary of the first result
            try:
                result = wikipedia.summary(search_results[0], auto_suggest=False)
            except wikipedia.DisambiguationError as e:
                # If disambiguation, try the first option
                result = wikipedia.summary(e.options[0], auto_suggest=False)
            except wikipedia.PageError:
                # If page not found (rare after search), try next result
                if len(search_results) > 1:
                    result = wikipedia.summary(search_results[1], auto_suggest=False)
                else:
                    result = "No information found."
            
            cache[cache_key] = result
            return result
        except Exception as e:
            self.logger.log(f"Error searching Wikipedia for {query}: {e}")
            return cache.get(cache_key, "No information found.")