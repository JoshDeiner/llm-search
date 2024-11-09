# services/web_search_service.py

import os
import logging
from typing import List

from src.constants import WEB_SEARCH_URL
from src.services.search_engine_service import SearchEngineService
from src.shared.types import SearchEngineResults

# WebSearchService -> name probably should be changed or combined


class WebSearchService:
    def __init__(self, web_search_url: str = WEB_SEARCH_URL) -> None:
        self.web_search_url = web_search_url
        self.se_service = SearchEngineService(host=web_search_url, engines=["brave"])

    def fetch_results(self, search_term: str) -> List[dict]:
        """Fetches search results for a given search term using the search engine service."""
        logging.info(f"Executing search query: {search_term}")

        # Use the search service to run the search query
        return self.se_service.run(search_term)
