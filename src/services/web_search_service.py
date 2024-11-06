# services/web_search_service.py

import os
import logging
from typing import List

from src.constants import WEB_SEARCH_URL
from src.services.search_engine_service import SearchEngineService

from src.shared.types import SearchEngineResults


class WebSearchService:
    def __init__(self, web_search_url: str = WEB_SEARCH_URL) -> None:
        self.web_search_url = web_search_url

    def fetch_results(self, search_term: str) -> SearchEngineResults:
        """Fetches search results for a given search term using the search engine service."""
        logging.info(f"Executing search query: {search_term}")
        
        # Initialize the search engine
        search_engine = SearchEngineService()
        
        # Run the search query and retrieve results
        search_results: SearchResults = search_engine.run(search_term, language="en-us")
        
        logging.info(f"Search results: {search_results}")
        # logging.info(f"Search type: {search_results}")
        logging.info(f"Search results (type: {type(search_results)}): {search_results}")



        # Change the name of return variable (optional for readability)
        return search_results
