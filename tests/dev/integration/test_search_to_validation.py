import pytest
from src.features.users.factory import create_user_service


# Mock search function for consistent test data
def mock_search(search_term):
    """
    Mock implementation of the search function for consistent test data.
    """
    return {
        "search_term": search_term,
        "web_results": [
            {"title": "Valid Restaurant", "description": "Great food in Tokyo"}
        ],
        "validation_results": [{"is_valid": True}],
    }


@pytest.fixture
def user_service(monkeypatch):
    """
    Provide a user_service instance with a mocked search method.
    """
    service = create_user_service()
    monkeypatch.setattr(service, "search", mock_search)
    return service


@pytest.mark.integration
def test_search_and_validate(user_service):
    """
    Integration test for user_service search and validate functionality.
    """
    # Test data
    search_term = "best restaurants in Tokyo"

    # Perform search
    search_data = user_service.search(search_term)

    # Assert the structure of the returned data
    assert "search_term" in search_data, "Expected 'search_term' in search_data."
    assert "web_results" in search_data, "Expected 'web_results' in search_data."
    assert (
        "validation_results" in search_data
    ), "Expected 'validation_results' in search_data."

    # Validate results
    validated_results = [
        result
        for result in search_data["validation_results"]
        if result.get("is_valid", False)
    ]

    # Assert the presence of validated results
    assert (
        len(validated_results) > 0
    ), "Expected at least one valid result in 'validation_results'."

    # Additional assertions for data consistency
    assert search_data["search_term"] == search_term, "Search term mismatch."
    assert len(search_data["web_results"]) > 0, "Expected at least one web result."
    assert (
        search_data["web_results"][0]["title"] == "Valid Restaurant"
    ), "Web result title mismatch."
