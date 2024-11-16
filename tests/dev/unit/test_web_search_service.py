import pytest
from src.shared.services.web_search_service import WebSearchService

@pytest.fixture
def web_search_service() -> WebSearchService:
    return WebSearchService()

def test_fetch_results(web_search_service: WebSearchService) -> None:
    # Act
    search_term = web_search_service.user_service.create_search_term("  Hello World  ")
    results = web_search_service.fetch_results(search_term)

    # Assert
    assert search_term == "hello world"
    assert isinstance(results, list)  # Assuming fetch_results returns a list of SearchResult