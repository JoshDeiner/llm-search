# services/search_validation_service.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
from keybert import KeyBERT
from difflib import SequenceMatcher


class SearchValidationService:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer()
        self.semantic_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.kw_model = KeyBERT("distilbert-base-nli-mean-tokens")

    def cosine_similarity_score(self, query: str, result_text: str) -> float:
        tfidf_matrix = self.tfidf_vectorizer.fit_transform([query, result_text])
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        return similarity_matrix[0][0]

    def semantic_similarity_score(self, query: str, result_text: str) -> float:
        query_embedding = self.semantic_model.encode(query, convert_to_tensor=True)
        result_embedding = self.semantic_model.encode(
            result_text, convert_to_tensor=True
        )
        similarity = util.cos_sim(query_embedding, result_embedding)
        return similarity.item()

    def keyword_coverage_score(
        self, query: str, result_text: str, top_n: int = 5
    ) -> float:
        query_keywords = [
            word for word, _ in self.kw_model.extract_keywords(query, top_n=top_n)
        ]
        result_keywords = [
            word for word, _ in self.kw_model.extract_keywords(result_text, top_n=top_n)
        ]
        overlap_count = sum(1 for kw in query_keywords if kw in result_keywords)
        return overlap_count / len(query_keywords) if query_keywords else 1

    def validate(self, query: str, result_text: str, threshold: float = 0.6) -> dict:
        cosine_score = self.cosine_similarity_score(query, result_text)
        semantic_score = self.semantic_similarity_score(query, result_text)
        keyword_score = self.keyword_coverage_score(query, result_text)

        # Weighted average score
        score = (cosine_score * 0.3) + (semantic_score * 0.5) + (keyword_score * 0.2)

        return {
            "score": score,
            "is_valid": score >= threshold,
            "cosine_score": cosine_score,
            "semantic_score": semantic_score,
            "keyword_score": keyword_score,
            "reason": (
                "Meets relevance threshold"
                if score >= threshold
                else "Below relevance threshold"
            ),
        }