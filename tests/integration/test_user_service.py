import pytest
from src.user_service.user import User
from src.services.search_term_service import SearchTermService
from src.services.web_search_service import WebSearchService
from src.services.search_validation_service import SearchValidationService, ValidationResult


@pytest.fixture
def mock_user_service(monkeypatch):
    """
    Fixture to provide a User instance with mocked dependencies.
    """
    # Mock dependencies
    class MockSearchTermService:
        def create_search_term(self, user_input):
            return "test query"

    class MockWebSearchService:
        def fetch_results(self, search_term):
            return [{"snippet": "Result 1 snippet"}, {"snippet": "Result 2 snippet"}]

    class MockSearchValidationService:
        def validate(self, search_term, snippet):
            return snippet == "Result 1 snippet"  # Validate only the first snippet

    # Replace the real services with mocks
    monkeypatch.setattr("src.services.search_term_service.SearchTermService", MockSearchTermService)
    monkeypatch.setattr("src.services.web_search_service.WebSearchService", MockWebSearchService)
    monkeypatch.setattr("src.services.search_validation_service.SearchValidationService", MockSearchValidationService)

    # Create and return the User instance with mocked services
    return User(
        search_term_service=MockSearchTermService(),
        web_search_service=MockWebSearchService(),
        validation_service=MockSearchValidationService(),
    )


def test_user_search(mock_user_service):
    """
    Test the `search` method of the User class.
    """
    # Act
    user_input = "test input"
    result = mock_user_service.search(user_input)

    # Assert
    # Validate the structure of the returned data
    assert isinstance(result, dict), "Expected a dictionary as the result."
    assert "search_term" in result, "Missing 'search_term' in the result."
    assert "web_results" in result, "Missing 'web_results' in the result."
    assert "validation_results" in result, "Missing 'validation_results' in the result."

    # Validate individual fields
    assert result["search_term"] == "test query", "Search term mismatch."
    assert result["web_results"] == ["Result 1 snippet", "Result 2 snippet"], "Web results mismatch."
    assert result["validation_results"] == [True, False], "Validation results mismatch."


def test_user_search_empty_results(monkeypatch):
    """
    Test the `search` method with empty search results.
    """
    # Arrange
    class MockSearchTermService:
        def create_search_term(self, user_input):
            return "test query"

    class MockWebSearchService:
        def fetch_results(self, search_term):
            return []  # Return no results

    class MockSearchValidationService:
        def validate(self, search_term, snippet):
            return False

    # Replace the real services with mocks
    monkeypatch.setattr("src.services.search_term_service.SearchTermService", MockSearchTermService)
    monkeypatch.setattr("src.services.web_search_service.WebSearchService", MockWebSearchService)
    monkeypatch.setattr("src.services.search_validation_service.SearchValidationService", MockSearchValidationService)

    # Create the User instance
    user_service = User(
        search_term_service=MockSearchTermService(),
        web_search_service=MockWebSearchService(),
        validation_service=MockSearchValidationService(),
    )

    # Act
    user_input = "test input"
    result = user_service.search(user_input)

    # Assert
    assert isinstance(result, dict), "Expected a dictionary as the result."
    assert result["search_term"] == "test query", "Search term mismatch."
    assert result["web_results"] == [], "Expected no web results."
    assert result["validation_results"] == [], "Expected no validation results."
