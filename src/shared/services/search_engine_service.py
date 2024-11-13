from typing import List

from src.shared.config.constants import WEB_SEARCH_URL
from langchain_community.utilities import SearxSearchWrapper

from src.shared.config.types import SearchResult


class SearchEngineService:
    def __init__(
        self, host: str = WEB_SEARCH_URL, num_results: int = 3, engines: List[str] = []
    ):
        """
        Initializes the SearxNG search engine with a specified host and default number of results.
        :param host: The Searx host URL.
        :param num_results: Default number of results to fetch per query.
        """
        self._host = host  # Store host as a private attribute
        self._num_results = num_results  # Store num_results as a private attribute
        self._search_wrapper = SearxSearchWrapper(searx_host=host, k=num_results)
        self._engines = engines

    def run(self, query: str) -> List[SearchResult]:
        """Perform a search and return collected results."""
        results: List[SearchResult] = self._search_wrapper.results(
            query=query, num_results=self._num_results, engines=self._engines
        )

        return results
