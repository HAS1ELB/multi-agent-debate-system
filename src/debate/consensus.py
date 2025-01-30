from collections import Counter
from transformers import pipeline

class Consensus:
    def reach_consensus(arguments):
        counter = Counter(arguments)
        return counter.most_common(1)[0][0]


    def summarize_debate(arguments):
        summarizer = pipeline("summarization")
        summary = summarizer(" ".join(arguments), max_length=50, min_length=25, do_sample=False)
        return summary[0]["summary_text"]