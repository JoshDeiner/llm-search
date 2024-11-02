from difflib import SequenceMatcher
from keybert import KeyBERT
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class LLMCore:
    def __init__(self):
        self.kw_model = KeyBERT("distilbert-base-nli-mean-tokens")

    def extract_key_terms(self, text: str, top_n: int = 5) -> list:
        keywords = self.kw_model.extract_keywords(text, top_n=top_n)
        return [word for word, score in keywords]

    def generate_text(self, prompt: str) -> str:
        """Implements generate_text as expected by LLMCore."""
        response = self.model.generate_content(prompt)
        return response.text

    def summarize_text(self, text: str) -> str:
        """Summarizes the given text."""
        summary_prompt = f"Summarize the following:\n\n{text}"
        return self.generate_text(summary_prompt)

    def synonym_match_score(self, summary: str, key_terms: list) -> float:
        """Calculates a score for key term presence in summary using synonym/context matching."""
        if not key_terms:
            return 1.0

        tfidf = TfidfVectorizer().fit_transform([summary] + key_terms)
        similarity_matrix = cosine_similarity(tfidf[0:1], tfidf[1:])
        return np.mean(similarity_matrix)

    def validate_and_score_summary(
        self,
        summary: str,
        original_text: str,
        expectations: dict = None,
        max_retries: int = 3,
    ) -> dict:
        """Validates and scores the summarization result with a retry mechanism if it doesn't meet the threshold."""

        if expectations is None:
            expectations = {
                "min_word_count": 30,
                "threshold": 0.5,
                "key_terms": self.extract_key_terms(original_text, top_n=5),
            }

        for attempt in range(max_retries):
            # Criteria 1: Check minimum word count
            word_count = len(summary.split())
            if word_count < expectations.get("min_word_count", 0):
                return {"score": 0, "is_valid": False, "reason": "Summary is too short"}

            # Criteria 2: Synonym-based keyword coverage score
            key_terms = expectations.get("key_terms", [])
            keyword_coverage = self.synonym_match_score(summary, key_terms)

            # Criteria 3: Relevance score using SequenceMatcher
            relevance_score = SequenceMatcher(None, summary, original_text).ratio()

            # Weighted score with emphasis on relevance and keyword coverage
            score = (keyword_coverage * 0.5) + (relevance_score * 0.5)
            print(f"Attempt {attempt + 1}: score = {score}")

            # Check if the score meets the threshold
            if score >= expectations["threshold"]:
                return {
                    "score": score,
                    "is_valid": True,
                    "reason": "Summary meets expectations",
                }

            # Regenerate the summary for the next attempt if score doesn't meet threshold
            summary = self.summarize_text(original_text)

        # Final result if threshold was not met after retries
        return {
            "score": score,
            "is_valid": False,
            "reason": "Summary did not meet relevance threshold after max retries",
        }
