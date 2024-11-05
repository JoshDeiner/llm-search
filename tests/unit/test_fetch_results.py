import pytest
from services.web_search_service import WebSearchService
from constants import WEB_SEARCH_URL

@pytest.fixture
def search_service(monkeypatch):
    # Override WEB_SEARCH_URL to use a mock domain, avoiding real network endpoints during testing
    monkeypatch.setattr("constants.WEB_SEARCH_URL", "http://mockdomain.com")
    
    # Initialize the WebSearchService with the (mocked) constant
    service = WebSearchService(web_search_url=WEB_SEARCH_URL)

    # Mock fetch_results directly to return a specific response
    def mock_fetch_results(query):
        return [{"title": "Mock Result", "link": "http://example.com"}]

    # Apply the mock to fetch_results
    monkeypatch.setattr(service, "fetch_results", mock_fetch_results)
    return service

def test_fetch_results(search_service):
    results = search_service.fetch_results("mock query")
    assert results is not None
    assert isinstance(results, list)
    assert results[0]["title"] == "Mock Result"
    assert results[0]["link"] == "http://example.com"
