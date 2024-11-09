import pytest
from src.user_service.factory import get_user_service


# Mock the WebSearchService to provide consistent test data for the pipeline
def mock_web_search(query):
    return [
        {"title": "Mock Restaurant", "snippet": "Top-rated food in Tokyo"},
        {"title": "Mock Cafe", "snippet": "Best coffee in Tokyo"},
    ]


# Mock the SearchValidationService to mark results as valid
def mock_validate(search_term, result):
    return {"is_valid": True}


# Fixture to set up user_service with mocks for the web search and validation parts of the pipeline
@pytest.fixture
def user_service(monkeypatch):
    service = get_user_service()

    # Mock the fetch_results method in WebSearchService to return a fixed response
    monkeypatch.setattr(service.web_search_service, "fetch_results", mock_web_search)
    # Mock the validate method in SearchValidationService to always return valid results
    monkeypatch.setattr(service.validation_service, "validate", mock_validate)

    return service


def test_user_search_pipeline(user_service):
    search_term = "best restaurants in Tokyo"
    search_data = user_service.search(search_term)

    # Verify the pipeline structure and integration
    assert "search_term" in search_data
    assert search_data["search_term"] == search_term
    assert "web_results" in search_data
    assert isinstance(search_data["web_results"], list)
    assert len(search_data["web_results"]) > 0

    # Check that validation results are included and at least one is marked as valid
    assert "validation_results" in search_data
    assert isinstance(search_data["validation_results"], list)
    validated_results = [
        result
        for result in search_data["validation_results"]
        if result.get("is_valid", False)
    ]
    assert len(validated_results) > 0  # At least one result should be valid
