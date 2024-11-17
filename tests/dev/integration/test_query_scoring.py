"""
This module contains integration tests for the interactions between WebSearchService,
QueryValidationService, and SearchEngineService. The tests cover various scenarios to ensure
that the User class correctly generates queries, validates them, and interacts with the search
engine service.

Test scenarios include:
- No data input: Ensures the system handles empty input gracefully.
- Strange data input: Tests the system's response to unusual characters.
- Foreign language input: Verifies the system's handling of non-English input.
- Two correct instances: Checks the system's behavior when multiple valid results are returned.
- Interaction from UserService to SearchEngineService: Ensures the correct flow from user query
  generation to search engine service interaction.
"""

import pytest
from src.features.users.models.user import User
from src.shared.services.web_search_service import WebSearchService
from src.shared.services.search_validation_service import SearchValidationService, ValidationResult
from src.shared.services.search_engine_service import SearchEngineService
from src.features.users.services.user_service import UserService

@pytest.fixture
def web_search_service():
    return WebSearchService()

@pytest.fixture
def validation_service():
    return SearchValidationService()

@pytest.fixture
def search_engine_service():
    return SearchEngineService()

@pytest.fixture
def user_service(web_search_service, validation_service, search_engine_service):
    class MockUserService(UserService):
        def create_search_term(self, user_input):
            return "test query"

    return User(
        web_search_service=web_search_service,
        validation_service=validation_service,
        user_service=MockUserService(),  # Add the mocked UserService
    )

@pytest.mark.integration
def test_query_scoring_no_data(user_service):
    """
    Test the search functionality with no data input.
    """
    # Act
    user_input = ""
    result = user_service.search(user_input)

    # Assert
    assert result["search_term"] == ""
    assert result["web_results"] == []
    assert result["validation_results"] == []
    assert result["all_results"] == []

@pytest.mark.integration
def test_query_scoring_strange_data(user_service):
    """
    Test the search functionality with strange data input.
    The input is semantically meaningless and should return nothing.
    """
    # Act
    user_input = "@#$%^&*()"
    result = user_service.search(user_input)

    # Assert
    assert result["search_term"] == "@#$%^&*()"
    assert result["web_results"] == []
    assert result["validation_results"] == []
    assert result["all_results"] == []

@pytest.mark.integration
def test_query_scoring_foreign_language(user_service):
    """
    Test the search functionality with foreign language input.
    Yes, the test `test_query_scoring_foreign_language` is designed to check how the system handles input in a foreign language (in this case, Japanese and Hebrew). The expectation that the search results, validation results, and all results are empty suggests that the system currently only supports English input.
    This test ensures that non-English input does not produce any results,
    indicating that the system is not yet equipped to handle foreign languages.
    """
    # Act
    japanese_input = "こんにちは、世界"
    hebrew_input = "שלום, עולם"
    japanese_result = user_service.search(japanese_input)
    hebrew_result = user_service.search(hebrew_input)

    # Assert
    assert japanese_result["search_term"] == "こんにちは、世界"
    assert japanese_result["web_results"] == []
    assert japanese_result["validation_results"] == []
    assert japanese_result["all_results"] == []

    assert hebrew_result["search_term"] == "שלום, עולם"
    assert hebrew_result["web_results"] == []
    assert hebrew_result["validation_results"] == []
    assert hebrew_result["all_results"] == []

@pytest.mark.integration
def test_query_scoring_two_correct_instances(user_service):
    """
    Test the search functionality with two correct instances.
    """
    # Arrange
    class MockWebSearchService(WebSearchService):
        def fetch_results(self, search_term):
            return [{"snippet": "Correct result 1"}, {"snippet": "Correct result 2"}]

    user_service.web_search_service = MockWebSearchService()

    # Act
    user_input = "test input"
    result = user_service.search(user_input)

    # Assert
    assert result["search_term"] == "test input"
    assert result["web_results"] == ["Correct result 1", "Correct result 2"]
    assert result["validation_results"] == [True, True]
    assert result["all_results"] == [{"snippet": "Correct result 1"}, {"snippet": "Correct result 2"}]

@pytest.mark.integration
def test_user_service_to_search_engine_service(user_service, search_engine_service):
    """
    Test the interaction from UserService to SearchEngineService.
    """
    # Arrange
    class MockSearchEngineService(SearchEngineService):
        def search(self, query):
            return [{"title": "Result 1"}, {"title": "Result 2"}]

    user_service.search_engine_service = MockSearchEngineService()

    # Act
    user_input = "test input"
    result = user_service.search(user_input)

    # Assert
    assert result["search_term"] == "test input"
    assert result["web_results"] == ["Result 1", "Result 2"]
    assert result["validation_results"] == [True, True]
    assert result["all_results"] == [{"title": "Result 1"}, {"title": "Result 2"}]