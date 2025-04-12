from .agent import Agent
from src.utils.cache import cache

class Economist(Agent):
    def __init__(self, name="Dr. Jones", use_api=False):
        super().__init__(name, expertise="Economics", use_api=use_api)

    def generate_argument(self, topic):
        cache_key = f"argument_{self.expertise}_{topic}"
        if cache_key in cache:
            return cache[cache_key]

        try:
            context = self.wikipedia.search(topic)
            if not context or "No information found" in context:
                context = "Use economic knowledge about the topic."
            prompt = (
                f"You are an economist. Provide a concise argument on {topic}, "
                f"focusing on economic costs, benefits, or market impacts. "
                f"Avoid repetition and ensure factual accuracy. Context: {context[:500]}"
            )
            for attempt in range(3):
                argument = self.generator(
                    prompt,
                    max_new_tokens=200,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    num_return_sequences=1,
                    pad_token_id=50256
                )[0]["generated_text"].strip()

                argument = argument.replace(prompt, "").strip()
                if not argument:
                    continue

                if not self._is_repetitive(argument) and len(argument.split()) > 20:
                    if len(argument.split()) > 100:
                        argument = self.summarize_response(argument)
                    cache[cache_key] = argument
                    return argument

            self.logger.log(f"Failed to generate non-repetitive argument for {self.name}.")
            return "Unable to generate a coherent argument."
        except Exception as e:
            self.logger.log(f"Error generating argument for {self.name}: {e}")
            return f"Unable to generate argument: {str(e)}"