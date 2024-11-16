import pytest
from src.features.search.query_scoring import QueryScoring, SearchEngine

class FakeSearchEngine(SearchEngine):
    """
    A fake implementation of a search engine for testing purposes.
    """

    def __init__(self) -> None:
        self.queries = []

    def search(self, query: str) -> str:
        self.queries.append(query)
        if "hi bob" in query.lower():
            return "Query rejected: irrelevant to project goals"
        return "Valid search result"


@pytest.fixture
def fake_search_engine() -> FakeSearchEngine:
    return FakeSearchEngine()


@pytest.fixture
def query_scoring() -> QueryScoring:
    return QueryScoring(threshold=0.5)


def test_scoring_algorithm(query_scoring: QueryScoring) -> None:
    # Act
    score = query_scoring.score_query("relevant query about project")

    # Assert
    assert score > 0.5

    # Act
    score = query_scoring.score_query("hi bob")

    # Assert
    assert score < 0.5


def test_threshold_score(query_scoring: QueryScoring) -> None:
    # Act & Assert
    assert query_scoring.is_query_relevant("relevant query about project") is True
    assert query_scoring.is_query_relevant("hi bob") is False


def test_integration_with_search_engine(query_scoring: QueryScoring, fake_search_engine: FakeSearchEngine) -> None:
    # Act
    result = query_scoring.search_with_validation(fake_search_engine, "hi bob")

    # Assert
    assert result == "Query rejected: irrelevant to project goals"
    assert len(fake_search_engine.queries) == 1
    assert fake_search_engine.queries[0] == "hi bob"

    # Act
    result = query_scoring.search_with_validation(fake_search_engine, "relevant query about project")

    # Assert
    assert result == "Valid search result"
    assert len(fake_search_engine.queries) == 2
    assert fake_search_engine.queries[1] == "relevant query about project"