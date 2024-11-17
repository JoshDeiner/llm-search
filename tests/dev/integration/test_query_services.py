"""
This module contains integration tests for the QueryValidationService and interactions between WebSearchService,
QueryValidationService, and SearchEngineService. The tests cover various scenarios to ensure
that the User class correctly generates queries, validates them, and interacts with the search
engine service.

Test scenarios include:
- Valid query: Ensures the system correctly scores and validates a valid query, and proceeds to search services.
- Invalid query: Ensures the system correctly identifies and handles an invalid query, and does not proceed to search services.
- Edge cases: Tests the system's response to edge cases such as empty or strange queries.
- No data input: Ensures the system handles empty input gracefully.
- Strange data input: Tests the system's response to unusual characters.
- Foreign language input: Verifies the system's handling of non-English input.
- Two correct instances: Checks the system's behavior when multiple valid results are returned.
- Interaction from UserService to SearchEngineService: Ensures the correct flow from user query generation to search engine service interaction.
"""

import pytest
from src.features.users.models.user import User
from src.shared.services.web_search_service import WebSearchService
from src.shared.services.search_validation_service import SearchValidationService, ValidationResult
from src.shared.services.search_engine_service import SearchEngineService
from src.features.users.services.user_service import UserService
from src.features.users.services.query_validation_service import QueryValidationService

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
def query_validation_service():
    return QueryValidationService()

@pytest.fixture
def user_service(web_search_service, validation_service, search_engine_service, query_validation_service):
    class MockUserService(UserService):
        def create_search_term(self, user_input):
            return "test query"

    return User(
        web_search_service=web_search_service,
        validation_service=validation_service,
        user_service=MockUserService(),  # Add the mocked UserService
        query_validation_service=query_validation_service
    )

class NetworkError(Exception):
    """Custom exception for network-related errors."""
    pass

@pytest.mark.integration
def test_query_validation_service_valid_query(user_service, query_validation_service):
    """
    Test the full flow with a valid query.
    """
    # Act
    query = "what year did Bell Labs begin its program"
    query_validation_score = query_validation_service.query_validator(query)
    
    # Check the validation score and decide the next step
    if query_validation_score == 0:
        # If the score is 0, raise a NetworkError
        raise NetworkError("Query validation score is 0, indicating an invalid query or network issue.")
    elif query_validation_score > 0.5:
        # If the score is greater than 0.5, proceed to search service
        result = user_service.search(query)
    else:
        # If the score is between 0 and 0.5, raise a ValueError
        raise ValueError("Query validation score is between 0 and 0.5, indicating a low-quality query.")

    # Assert
    assert result is not None, "Expected the query to proceed to search services."
    assert result["search_term"] == "valid query"
    assert "web_results" in result
    assert "validation_results" in result
    assert "all_results" in result


@pytest.mark.integration
def test_failing_query_score(user_service, query_validation_service):
    """
    Test the full flow with multiple queries.
    """
    queries = [
        "useless tools",
        "@#$%^&*()",
        ""
    ]

    for query in queries:
        query_validation_score = query_validation_service.query_validator(query)
        assert query_validation_score < 0.51, f"Expected the query '{query}' to have a validation score of 0."
       

@pytest.mark.integration
def test_query_validation_service_failing_queries(user_service, query_validation_service):
    """
    Test the full flow with multiple queries.
    """
    queries = [
        "useless tools",
        "what year did Bell Labs begin its program",
        "@#$%^&*()",
        ""
    ]

    for query in queries:
        # Act
        query_validation_score = query_validation_service.query_validator(query)
        
        # Check the validation score and decide the next step
        if query_validation_score == 0:
            # If the score is 0, raise a NetworkError
            raise NetworkError(f"Query validation score is 0 for query '{query}', indicating an invalid query or network issue.")
        elif query_validation_score > 0.5:
            # If the score is greater than 0.5, proceed to search service
            result = user_service.search(query)
        else:
            # If the score is between 0 and 0.5, raise a ValueError
            raise ValueError(f"Query validation score is between 0 and 0.5 for query '{query}', indicating a low-quality query.")

        # Assert
        assert result is not None, f"Expected the query '{query}' to proceed to search services."
        assert result["search_term"] == query
        assert "web_results" in result
        assert "validation_results" in result
        assert "all_results" in result

@pytest.mark.unit
def test_query_scoring_no_data(user_service):
    """
    Test the search functionality with no data input.
    """

    queries = [
        "",
        "@#$%^&*()",
        "useless tools"
    ]

    for query in queries:
        is_valid = user_service._user_service.validate_input(query)
        # Assert
        assert not is_valid, "Expected the input to be invalid when empty."

@pytest.mark.integration
def test_query_scoring_two_correct_instances(user_service):
    """
    Test the search functionality with two correct instances.
    """
    # Arrange
    class MockWebSearchService(WebSearchService):
        def fetch_results(self, search_term):
            return [
                {
                    "snippet": "Correct result 1",
                    "title": "Title 1",
                    "link": "http://example.com/1",
                    "engines": ["engine1"],
                    "category": "category1"
                },
                {
                    "snippet": "Correct result 2",
                    "title": "Title 2",
                    "link": "http://example.com/2",
                    "engines": ["engine2"],
                    "category": "category2"
                }
            ]

    user_service.web_search_service = MockWebSearchService()

    # Act
    user_input = "test input"
    result = user_service.search(user_input)

    # Assert
    assert result["search_term"] == "test input"
    assert result["web_results"] == ["Correct result 1", "Correct result 2"]
    assert result["validation_results"] == [True, True]
    assert result["all_results"] == [
        {
            "snippet": "Correct result 1",
            "title": "Title 1",
            "link": "http://example.com/1",
            "engines": ["engine1"],
            "category": "category1"
        },
        {
            "snippet": "Correct result 2",
            "title": "Title 2",
            "link": "http://example.com/2",
            "engines": ["engine2"],
            "category": "category2"
        }
    ]

@pytest.mark.integration
def test_user_service_to_search_engine_service(user_service, search_engine_service):
    """
    Test the interaction from UserService to SearchEngineService.
    """
    # Arrange
    class MockSearchEngineService(SearchEngineService):
        def run(self, query):
            return [
                {
                    "snippet": "Result 1 snippet",
                    "title": "Result 1",
                    "link": "http://example.com/1",
                    "engines": ["engine1"],
                    "category": "category1"
                },
                {
                    "snippet": "Result 2 snippet",
                    "title": "Result 2",
                    "link": "http://example.com/2",
                    "engines": ["engine2"],
                    "category": "category2"
                }
            ]

    user_service.search_engine_service = MockSearchEngineService()

    # Act
    user_input = "test input"
    result = user_service.search(user_input)

    # Assert
    assert result["search_term"] == "test input"
    assert result["web_results"] == ["Result 1 snippet", "Result 2 snippet"]
    assert result["validation_results"] == [True, True]
    assert result["all_results"] == [
        {
            "snippet": "Result 1 snippet",
            "title": "Result 1",
            "link": "http://example.com/1",
            "engines": ["engine1"],
            "category": "category1"
        },
        {
            "snippet": "Result 2 snippet",
            "title": "Result 2",
            "link": "http://example.com/2",
            "engines": ["engine2"],
            "category": "category2"
        }
    ]

@pytest.mark.integration
def test_query_validation_service_query_scores(query_validation_service):
    """
    Test the query validation service to check the scores of multiple queries.
    """
    queries = [
        "useless tools",
        "what year did Bell Labs begin its program",
        "@#$%^&*()",
        ""
    ]

    for query in queries:
        # Act
        query_validation_score = query_validation_service.query_validator(query)
        
        # Assert
        assert isinstance(query_validation_score, float), f"Expected a float score for query '{query}'."
        assert 0 <= query_validation_score <= 1, f"Expected the score to be between 0 and 1 for query '{query}'."

