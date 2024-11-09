# tests/unit/test_search_engine_service.py

import pytest
from unittest.mock import patch
from src.services.search_engine_service import SearchEngineService

class TestSearchEngineService:

    @patch('src.services.search_engine_service.SearxSearchWrapper')
    def test_initialization(self, MockSearxSearchWrapper):
        # Arrange
        mock_instance = MockSearxSearchWrapper.return_value

        # Act
        service = SearchEngineService(host="http://localhost:8080", num_results=5, engines=["brave"])

        # Assert
        assert service._host == "http://localhost:8080"
        assert service._num_results == 5
        assert service._search_wrapper == mock_instance

    @patch('src.services.search_engine_service.SearxSearchWrapper')
    def test_run_method(self, MockSearxSearchWrapper):
        # Arrange
        mock_instance = MockSearxSearchWrapper.return_value
        mock_instance.results.return_value = [
            {'title': 'Title 1', 'link': 'http://example.com/1', 'snippet': 'Snippet 1'},
            {'title': 'Title 2', 'link': 'http://example.com/2', 'snippet': 'Snippet 2'},
        ]

        service = SearchEngineService(engines=["brave"])

        # Act
        results = service.run("landmarks in Paris")

        # Assert
        assert len(results) == 2
        assert results[0]['title'] == 'Title 1'
        assert results[1]['link'] == 'http://example.com/2'
        assert results[0]['snippet'] == 'Snippet 1'
        assert results[1]['snippet'] == 'Snippet 2'
        mock_instance.results.assert_called_once_with(query="landmarks in Paris", num_results=3, engines=["brave"])

# This allows running the test directly from the script
if __name__ == '__main__':
    pytest.main()
