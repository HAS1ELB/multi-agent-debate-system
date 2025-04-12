from transformers import pipeline
from src.fact_checking.retrieval import Retrieval
from src.utils.logger import Logger

class FactChecker:
    def __init__(self):
        self.logger = Logger()
        try:
            self.classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-base",
                device=-1
            )
            self.retrieval = Retrieval()
        except Exception as e:
            self.logger.log(f"Error initializing FactChecker: {e}")
            self.classifier = None

    def check_fact(self, claim):
        if not claim or "Error" in claim or "Unable" in claim or self.classifier is None:
            self.logger.log(f"Invalid claim or classifier not initialized: {claim}")
            return {"claim": claim, "verdict": "Invalid", "confidence": 0.0, "context": ""}

        try:
            context = self.retrieval.retrieve(claim)
            if not context or "No information found" in context or "Error" in context:
                context = "No reliable information available."
            
            # Split claim into sentences for finer-grained checking
            sentences = [s.strip() for s in claim.split(". ") if s.strip()]
            verdicts = []
            confidences = []

            for sentence in sentences:
                result = self.classifier(
                    sentence,
                    candidate_labels=["True", "False", "Uncertain"],
                    hypothesis_template="This statement is {}.",
                    multi_label=False
                )
                verdicts.append(result["labels"][0])
                confidences.append(result["scores"][0])

            # Aggregate verdicts
            if all(v == "True" for v in verdicts):
                final_verdict = "True"
                confidence = sum(confidences) / len(confidences)
            elif any(v == "False" for v in verdicts):
                final_verdict = "False"
                confidence = max(c for c, v in zip(confidences, verdicts) if v == "False")
            else:
                final_verdict = "Uncertain"
                confidence = max(confidences)

            return {
                "claim": claim,
                "verdict": final_verdict,
                "confidence": confidence,
                "context": context[:200]
            }
        except Exception as e:
            self.logger.log(f"Error checking fact for claim '{claim}': {e}")
            return {
                "claim": claim,
                "verdict": "Error",
                "confidence": 0.0,
                "context": f"Error retrieving context: {str(e)}"
            }