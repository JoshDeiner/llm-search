# services/web_search_service.py

import logging
from typing import List

from src.shared.config.constants import WEB_SEARCH_URL
from src.shared.services.search_engine_service import SearchEngineService
from src.features.users.user_service import UserService

from src.shared.config.types import SearchResult


class WebSearchService:
    def __init__(self, web_search_url: str = WEB_SEARCH_URL) -> None:
        self.web_search_url = web_search_url
        self.se_service = SearchEngineService(host=web_search_url, engines=["brave"])
        self.user_service = UserService()

    def fetch_results(self, search_term: str) -> List[SearchResult]:
        """Fetches search results for a given search term using the search engine service."""
        logging.info(f"Executing search query: {search_term}")
        # Use the search service to run the search query
        results: List[SearchResult] = self.se_service.run(
            self.user_service.create_search_term(search_term)
        )
        return results
