import wikipediaapi
from src.utils.logger import Logger
from src.utils.cache import cache

class Wikipedia:
    def __init__(self, language='en'):
        self.wiki_wiki = wikipediaapi.Wikipedia(
            language=language,
            user_agent='MultiAgentDebateSystem/1.0'
        )
        self.logger = Logger()

    def search(self, query):
        cache_key = f"wiki_{query}"
        if cache_key in cache:
            return cache[cache_key]

        try:
            page = self.wiki_wiki.page(query)
            result = page.summary if page.exists() else "No information found."
            cache[cache_key] = result
            return result
        except Exception as e:
            self.logger.log(f"Error searching Wikipedia for {query}: {e}")
            return cache.get(cache_key, "No information found.")