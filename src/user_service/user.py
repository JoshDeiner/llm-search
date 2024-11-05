# user_service/user.py

from services.search_term_service import SearchTermService
from services.web_search_service import WebSearchService
from services.search_validation_service import SearchValidationService


class User:
    def __init__(
        self,
        search_term_service: SearchTermService,
        web_search_service: WebSearchService,
        validation_service: SearchValidationService,
    ) -> None:
        self.search_term_service = search_term_service
        self.web_search_service = web_search_service
        self.validation_service = validation_service

    def search(self, user_input: str) -> dict:
        """Creates a search term, fetches results, and validates relevance."""
        search_term = self.search_term_service.create_search_term(user_input)
        web_results = self.web_search_service.fetch_results(search_term)

        # Validate each result against the query
        validation_results = [
            self.validation_service.validate(search_term, result)
            for result in web_results
        ]

        return {
            "search_term": search_term,
            "web_results": web_results,
            "validation_results": validation_results,
        }
