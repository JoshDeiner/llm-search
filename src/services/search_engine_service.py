import os
from typing import List
from typing import Dict


from src.constants import WEB_SEARCH_URL
from langchain_community.utilities import SearxSearchWrapper

class SearchEngineService:
    def __init__(self, host: str = WEB_SEARCH_URL, num_results: int = 3):
        """
        Initializes the SearxNG search engine with a specified host and default number of results.
        :param host: The Searx host URL.
        :param num_results: Default number of results to fetch per query.
        """
        self._host = host  # Store host as a private attribute
        self._num_results = num_results  # Store num_results as a private attribute
        self._search_wrapper = SearxSearchWrapper(searx_host=host, k=num_results)

    def run(self, query: str) -> List[Dict]:
        """Perform a search and return collected results."""
        results = self._search_wrapper.results(  # Use the correct private attribute
            query=query,
            num_results=self._num_results
        )
        return results
