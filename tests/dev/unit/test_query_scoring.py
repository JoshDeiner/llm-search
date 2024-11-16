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
    """
    Test the scoring algorithm to ensure it correctly scores queries.
    """
    # Act
    score = query_scoring.score_query("relevant query about project")

    # Assert
    assert score > 0.5

    # Act
    score = query_scoring.score_query("hi bob")

    # Assert
    assert score < 0.5


def test_threshold_score(query_scoring: QueryScoring) -> None:
    """
    Test the threshold score to ensure queries are correctly classified as relevant or irrelevant.
    """
    # Act & Assert
    assert query_scoring.is_query_relevant("relevant query about project") is True
    assert query_scoring.is_query_relevant("hi bob") is False


def test_integration_with_search_engine(query_scoring: QueryScoring, fake_search_engine: FakeSearchEngine) -> None:
    """
    Test the integration of the query scoring system with the search engine.
    """
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


def test_good_query_score(query_scoring: QueryScoring) -> None:
    """
    Test that a good query receives a high score.
    """
    # Act
    score = query_scoring.score_query("who did the new york yankees play in the world series")

    # Assert
    assert score > 0.5


def test_bad_query_score(query_scoring: QueryScoring) -> None:
    """
    Test that a bad query receives a low score.
    """
    # Act
    score = query_scoring.score_query("hi bob")

    # Assert
    assert score < 0.5


def test_empty_query_score(query_scoring: QueryScoring) -> None:
    """
    Test the scoring algorithm with  (empty query).
    empty query should return 0.0
    """
    # Act
    score = query_scoring.score_query("")

    # Assert
    assert score == 0.0


def test_unclear_query_score(query_scoring: QueryScoring) -> None:
    """
    Test that an unclear query receives a score equal to the threshold.
    """
    # Act
    # replace with query that is neither good nor bad and probably should fail
    score = query_scoring.score_query("unclear query")

    # Assert
    assert score == 0.5  # Assuming 0.5 is the threshold score


