from transformers import pipeline
from diskcache import Cache
from src.knowledge.data_sources.wikipedia import Wikipedia

# Initialisez le cache
cache = Cache("data/knowledge_cache")

class Agent:
    def __init__(self, name, expertise):
        self.name = name
        self.expertise = expertise
        self.generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M", device="cpu")
        self.summarizer = pipeline("summarization")
        self.wikipedia = Wikipedia()

    def generate_argument(self, topic):
        cache_key = f"argument_{self.expertise}_{topic}"
        if cache_key in cache:
            return cache[cache_key]

        # Récupérer des informations de Wikipedia
        context = self.wikipedia.search(topic)
        prompt = f"As a {self.expertise}, provide a well-structured and detailed argument about {topic}. Use the following context: {context}"

        # Générer l'argument
        argument = self.generator(prompt, max_new_tokens=150, temperature=0.7, top_p=0.9, truncation=True)[0]["generated_text"]

        # Vérifier les répétitions
        if self._is_repetitive(argument):
            argument = self.generator(prompt, max_new_tokens=150, temperature=0.7, top_p=0.9, truncation=True)[0]["generated_text"]

        # Résumer l'argument si nécessaire
        if len(argument.split()) > 100:
            argument = self.summarize_response(argument)

        cache[cache_key] = argument
        return argument

    def evaluate_argument(self, argument):
        cache_key = f"evaluation_{self.expertise}_{argument}"
        if cache_key in cache:
            return cache[cache_key]

        prompt = f"Evaluate this argument from the perspective of {self.expertise}: {argument}"
        evaluation = self.generator(prompt, max_new_tokens=150, temperature=0.7, top_p=0.9, truncation=True)[0]["generated_text"]
        cache[cache_key] = evaluation
        return evaluation

    def _is_repetitive(self, text):
        sentences = text.split(". ")
        if len(sentences) > 1 and sentences[0] == sentences[1]:
            return True
        return False

    def summarize_response(self, response):
        summary = self.summarizer(response, max_length=50, min_length=25, do_sample=False)
        return summary[0]["summary_text"]