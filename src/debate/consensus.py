from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from src.utils.logger import Logger

class Consensus:
    def __init__(self):
        self.logger = Logger()
        try:
            self.summarizer = pipeline("summarization", model="facebook/bart-base")
            self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            self.logger.log(f"Error initializing Consensus: {e}")
            self.summarizer = None

    def reach_consensus(self, arguments):
        try:
            valid_args = [
                arg for arg in arguments
                if arg and "Error" not in arg and "Unable" not in arg and len(arg.strip()) > 20
            ]
            if not valid_args:
                self.logger.log("No valid arguments for consensus.")
                return "No consensus reached: no valid arguments provided."

            # Find semantically similar arguments
            embeddings = self.similarity_model.encode(valid_args, batch_size=8)
            similarities = util.cos_sim(embeddings, embeddings)
            common_points = []
            used_indices = set()

            for i in range(len(valid_args)):
                if i in used_indices:
                    continue
                similar_args = [
                    valid_args[j] for j in range(len(valid_args))
                    if similarities[i][j] > 0.75 and i != j and j not in used_indices
                ]
                if similar_args:
                    common_points.append(valid_args[i])
                    used_indices.add(i)
                    used_indices.update(
                        j for j in range(len(valid_args)) if similarities[i][j] > 0.75
                    )

            if not common_points:
                return "No consensus reached: arguments are too divergent."

            return self.summarize_debate(common_points)
        except Exception as e:
            self.logger.log(f"Error reaching consensus: {e}")
            return f"Unable to reach consensus: {str(e)}"

    def summarize_debate(self, arguments):
        if self.summarizer is None:
            self.logger.log("Summarizer not initialized.")
            return " ".join(arguments)[:100]

        try:
            combined_text = " ".join(arguments)
            if len(combined_text.split()) < 10:
                return combined_text
            summary = self.summarizer(
                combined_text,
                max_length=60,
                min_length=20,
                do_sample=False
            )[0]["summary_text"].strip()
            return summary
        except Exception as e:
            self.logger.log(f"Error summarizing debate: {e}")
            return " ".join(arguments)[:100]