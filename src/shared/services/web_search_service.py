# services/web_search_service.py

import logging
from typing import List

from src.shared.config.constants import WEB_SEARCH_URL
from src.shared.services.search_engine_service import SearchEngineService

class WebSearchService:
    def __init__(self, web_search_url: str = WEB_SEARCH_URL) -> None:
        self.web_search_url = web_search_url
        self.se_service = SearchEngineService(host=web_search_url, engines=["brave"])

    def sanitize_input(self, user_input: str) -> str:
        """Sanitizes user input by stripping whitespace and converting to lowercase."""
        return user_input.strip().lower()

    def create_search_term(self, user_input: str) -> str:
        """Generates a search term based on user input."""
        sanitized_input = self.sanitize_input(user_input)
        return sanitized_input

    def fetch_results(self, search_term: str) -> List[dict]:
        """Fetches search results for a given search term using the search engine service."""
        logging.info(f"Executing search query: {search_term}")
        # Use the search service to run the search query
        return self.se_service.run(search_term)
