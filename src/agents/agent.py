from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from src.knowledge.data_sources.wikipedia import Wikipedia
from src.utils.logger import Logger
from src.utils.cache import cache
from src.utils.config import Config

class Agent:
    def __init__(self, name, expertise, use_api=False):
        self.name = name
        self.expertise = expertise
        self.logger = Logger()
        self.wikipedia = Wikipedia()
        self.use_api = use_api
        try:
            if use_api:
                from openai import OpenAI
                self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
                self.generator = self._api_generate
            else:
                self.generator = pipeline(
                    "text-generation",
                    model="EleutherAI/gpt-neo-125M",
                    device=-1
                )
            self.summarizer = pipeline("summarization", model="facebook/bart-base")
            self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            self.logger.log(f"Error initializing pipelines for {self.name}: {e}")
            raise

    def generate_argument(self, topic):
        cache_key = f"argument_{self.expertise}_{topic}"
        if cache_key in cache:
            return cache[cache_key]

        try:
            context = self.wikipedia.search(topic)
            if not context or "No information found" in context:
                context = "Use general knowledge about the topic."
            prompt = (
                f"You are a {self.expertise} expert. Provide a clear, concise, and fact-based argument on {topic}. "
                f"Focus on unique insights relevant to your expertise, avoid repetition, and ensure factual accuracy. "
                f"Context: {context[:500]}"
            )
            for attempt in range(3):  # Retry up to 3 times
                argument = self.generator(
                    prompt,
                    max_new_tokens=150,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    num_return_sequences=1,
                    pad_token_id=50256  # EOS token for GPT-Neo
                )[0]["generated_text"].strip()

                # Clean up output
                argument = argument.replace(prompt, "").strip()
                if not argument:
                    continue

                # Check for repetition and coherence
                if not self._is_repetitive(argument) and len(argument.split()) > 20:
                    if len(argument.split()) > 100:
                        argument = self.summarize_response(argument)
                    cache[cache_key] = argument
                    return argument

            self.logger.log(f"Failed to generate non-repetitive argument for {self.name} after 3 attempts.")
            return "Unable to generate a coherent argument."
        except Exception as e:
            self.logger.log(f"Error generating argument for {self.name} on {topic}: {e}")
            return f"Unable to generate argument: {str(e)}"

    def evaluate_argument(self, argument):
        cache_key = f"evaluation_{self.expertise}_{argument[:50].replace(' ', '_')}"
        if cache_key in cache:
            return cache[cache_key]

        if not argument or "Error" in argument or "Unable" in argument:
            return "Cannot evaluate invalid argument."

        try:
            prompt = (
                f"As a {self.expertise} expert, critically evaluate this argument: '{argument}'. "
                f"Provide a concise critique, highlighting one strength and one weakness. Avoid repetition."
            )
            for attempt in range(3):
                evaluation = self.generator(
                    prompt,
                    max_new_tokens=100,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    num_return_sequences=1,
                    pad_token_id=50256
                )[0]["generated_text"].strip()

                evaluation = evaluation.replace(prompt, "").strip()
                if not evaluation:
                    continue

                if not self._is_repetitive(evaluation) and len(evaluation.split()) > 15:
                    cache[cache_key] = evaluation
                    return evaluation

            self.logger.log(f"Failed to generate non-repetitive evaluation for {self.name}.")
            return "Unable to provide a coherent evaluation."
        except Exception as e:
            self.logger.log(f"Error evaluating argument for {self.name}: {e}")
            return f"Unable to evaluate argument: {str(e)}"

    def _is_repetitive(self, text):
        sentences = [s.strip() for s in text.split(". ") if s.strip()]
        if len(sentences) < 2:
            return len(sentences) == 0
        embeddings = self.similarity_model.encode(sentences, batch_size=8)
        for i in range(len(embeddings)-1):
            if util.cos_sim(embeddings[i], embeddings[i+1])[0][0] > 0.85:
                return True
        # Check for repeated phrases
        words = text.lower().split()
        for i in range(len(words)-4):
            phrase = " ".join(words[i:i+4])
            if text.lower().count(phrase) > 2:
                return True
        return False

    def summarize_response(self, response):
        try:
            if not response.strip():
                return response
            summary = self.summarizer(
                response,
                max_length=50,
                min_length=20,
                do_sample=False
            )[0]["summary_text"].strip()
            return summary
        except Exception as e:
            self.logger.log(f"Error summarizing response for {self.name}: {e}")
            return response[:100]

    def _api_generate(self, prompt, **kwargs):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_new_tokens", 150),
                temperature=kwargs.get("temperature", 0.7),
                top_p=kwargs.get("top_p", 0.9)
            )
            return [{"generated_text": response.choices[0].message.content.strip()}]
        except Exception as e:
            self.logger.log(f"OpenAI API error for {self.name}: {e}")
            return [{"generated_text": f"API error: {str(e)}"}]