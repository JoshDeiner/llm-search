# src/shared/services/search_validation_service.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from sentence_transformers import util
from keybert import KeyBERT
from typing import TypedDict


class ValidationResult(TypedDict):
    score: float
    is_valid: bool
    cosine_score: float
    semantic_score: float
    keyword_score: float
    reason: str


class SearchValidationService:
    def __init__(self) -> None:
        self.tfidf_vectorizer: TfidfVectorizer = TfidfVectorizer()
        self.semantic_model: SentenceTransformer = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )
        self.kw_model: KeyBERT = KeyBERT("distilbert-base-nli-mean-tokens")

    def cosine_similarity_score(self, query: str, result_text: str) -> float:
        tfidf_matrix = self.tfidf_vectorizer.fit_transform([query, result_text])
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        cosine_similarity_score: float = similarity_matrix[0][0]
        return cosine_similarity_score

    def semantic_similarity_score(self, query: str, result_text: str) -> float:
        query_embedding = self.semantic_model.encode(query, convert_to_tensor=True)
        result_embedding = self.semantic_model.encode(
            result_text, convert_to_tensor=True
        )
        similarity = util.cos_sim(query_embedding, result_embedding)
        similarity_score: float = similarity.item()
        return similarity_score

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
        return overlap_count / len(query_keywords) if query_keywords else 1.0

    def validate(
        self, query: str, result_text: str, threshold: float = 0.6
    ) -> ValidationResult:
        cosine_score: float = self.cosine_similarity_score(query, result_text)
        semantic_score: float = self.semantic_similarity_score(query, result_text)
        keyword_score: float = self.keyword_coverage_score(query, result_text)

        # Weighted average score
        score: float = (
            (cosine_score * 0.3) + (semantic_score * 0.5) + (keyword_score * 0.2)
        )

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
