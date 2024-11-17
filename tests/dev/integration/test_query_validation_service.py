"""
This module contains integration tests for the QueryValidationService.
The tests cover various scenarios to ensure that the service correctly scores and validates queries,
and integrates with WebSearchService and SearchEngineService.

Test scenarios include:
- Valid query: Ensures the system correctly scores and validates a valid query, and proceeds to search services.
- Invalid query: Ensures the system correctly identifies and handles an invalid query, and does not proceed to search services.
- Edge cases: Tests the system's response to edge cases such as empty or strange queries.
"""

import pytest
from src.features.users.models.user import User
from src.shared.services.web_search_service import WebSearchService
from src.shared.services.search_validation_service import SearchValidationService
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

# @pytest.mark.integration
# def test_query_validation_service_invalid_query(user_service, query_validation_service):
#     """
#     Test the full flow with an invalid query.
#     """
#     # Act
#     query = ""
#     query_validation_score = query_validation_service.query_validator(query)
    
#     # Check the validation score and decide the next step
#     if query_validation_score == 0:
#         # If the score is 0, raise a NetworkError
#         raise NetworkError("Query validation score is 0, indicating an invalid query or network issue.")
#     elif query_validation_score > 0.5:
#         # If the score is greater than 0.5, proceed to search service
#         result = user_service.search(query)
#     else:
#         # If the score is between 0 and 0.5, raise a ValueError
#         raise ValueError("Query validation score is between 0 and 0.5, indicating a low-quality query.")

#     # Assert
#     assert result is None, "Expected the query to be blocked by the validation service."

# @pytest.mark.integration
# def test_query_validation_service_strange_query(user_service, query_validation_service):
#     """
#     Test the full flow with a strange query.
#     """
#     # Act
#     query = "@#$%^&*()"
#     query_validation_score = query_validation_service.query_validator(query)
    
#     # Check the validation score and decide the next step
#     if query_validation_score == 0:
#         # If the score is 0, raise a NetworkError
#         raise NetworkError("Query validation score is 0, indicating an invalid query or network issue.")
#     elif query_validation_score > 0.5:
#         # If the score is greater than 0.5, proceed to search service
#         result = user_service.search(query)
#     else:
#         # If the score is between 0 and 0.5, raise a ValueError
#         raise ValueError("Query validation score is between 0 and 0.5, indicating a low-quality query.")

#     # Assert
#     assert result is None, "Expected the query to be blocked by the validation service."

# @pytest.mark.integration
# def test_query_validation_service_not_detailed_query(user_service, query_validation_service):
#     """
#     Test the full flow with the query "useless tools".
#     """
#     # Act
#     query = "useless tools"
#     query_validation_score = query_validation_service.query_validator(query)
    
#     # Check the validation score and decide the next step
#     if query_validation_score == 0:
#         # If the score is 0, raise a NetworkError
#         raise NetworkError("Query validation score is 0, indicating an invalid query or network issue.")
#     elif query_validation_score > 0.5:
#         # If the score is greater than 0.5, proceed to search service
#         result = user_service.search(query)
#     else:
#         # If the score is between 0 and 0.5, raise a ValueError
#         raise ValueError("Query validation score is between 0 and 0.5, indicating a low-quality query.")

#     # Assert
#     assert result is not None, "Expected the query to proceed to search services."
#     assert result["search_term"] == "useless tools"
#     assert "web_results" in result
#     assert "validation_results" in result
#     assert "all_results" in result

@pytest.mark.integration
def test_query_validation_service_bad_failing_queries(user_service, query_validation_service):
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



# @pytest.mark.integration
# def test_query_validation_service_passing_queries(user_service, query_validation_service):
#     """
#     Test the full flow with multiple queries.
#     """
#     queries = [
#         "what year did Bell Labs begin its program"
#     ]

#     for query in queries:
#         # Act
#         query_validation_score = query_validation_service.query_validator(query)
        
#         # Check the validation score and decide the next step
#         if query_validation_score == 0:
#             # If the score is 0, raise a NetworkError
#             raise NetworkError(f"Query validation score is 0 for query '{query}', indicating an invalid query or network issue.")
#         elif query_validation_score > 0.5:
#             # If the score is greater than 0.5, proceed to search service
#             result = user_service.search(query)
#         else:
#             # If the score is between 0 and 0.5, raise a ValueError
#             raise ValueError(f"Query validation score is between 0 and 0.5 for query '{query}', indicating a low-quality query.")

#         # Assert
#         assert result is not None, f"Expected the query '{query}' to proceed to search services."
#         assert result["search_term"] == query
#         assert "web_results" in result
#         assert "validation_results" in result
#         assert "all_results" in result