import wikipediaapi

class Wikipedia:
    def __init__(self):
        self.wiki_wiki = wikipediaapi.Wikipedia(
            language='en',  # Langue de Wikipedia
            user_agent='MultiAgentDebateSystem/1.0'  # User agent générique
        )
    def search(self, query):
        page = self.wiki_wiki.page(query)
        return page.summary if page.exists() else "No information found."