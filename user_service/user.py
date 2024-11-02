# user_service/user.py

from services.search_term_service import SearchTermService
from services.web_search_service import WebSearchService


class User:
    def __init__(
        self,
        search_term_service: SearchTermService,
        web_search_service: WebSearchService,
    ):
        self.search_term_service = search_term_service
        self.web_search_service = web_search_service

    def search(self, user_input: str) -> list:
        """Creates a search term and fetches raw results from WebSearchService."""
        search_term = self.search_term_service.create_search_term(user_input)
        web_results = self.web_search_service.fetch_results(search_term)
        return web_results
