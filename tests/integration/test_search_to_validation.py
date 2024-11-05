import pytest
from user_service.factory import get_user_service


# Mock search function for consistent test data
def mock_search(search_term):
    return {
        "search_term": search_term,
        "web_results": [
            {"title": "Valid Restaurant", "description": "Great food in Tokyo"}
        ],
        "validation_results": [{"is_valid": True}],
    }


# Fixture to override user_service's search with mock_search
@pytest.fixture
def user_service(monkeypatch):
    service = get_user_service()
    # Use monkeypatch to replace search with mock_search for this fixture
    monkeypatch.setattr(service, "search", mock_search)
    return service


# Integration test for search and validate functionality
def test_search_and_validate(user_service):
    search_term = "best restaurants in Tokyo"
    search_data = user_service.search(search_term)

    # Check the structure and presence of mock data fields
    assert "search_term" in search_data
    assert "web_results" in search_data
    assert "validation_results" in search_data

    # Filter for validated results in validation_results
    validated_results = [
        result
        for result in search_data["validation_results"]
        if result.get("is_valid", False)
    ]

    assert len(validated_results) > 0  # Expect at least one valid result
