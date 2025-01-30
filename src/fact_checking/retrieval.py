import wikipediaapi

class Retrieval:
    def __init__(self):
        self.wiki_wiki = wikipediaapi.Wikipedia('en')

    def retrieve(self, query):
        page = self.wiki_wiki.page(query)
        return page.summary if page.exists() else "No information found."