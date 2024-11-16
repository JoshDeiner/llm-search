# user_service/user.py

from src.shared.services.web_search_service import WebSearchService

from src.shared.services.search_validation_service import SearchValidationService
from src.shared.services.search_validation_service import ValidationResult
from src.features.users.services.user_service import UserService
from typing import List

from src.shared.config.types import SearchResponse


class User:
    def __init__(
        self,
        web_search_service: WebSearchService,
        validation_service: SearchValidationService,
        user_service: UserService,
    ) -> None:
        self.web_search_service: WebSearchService = web_search_service
        self.validation_service: SearchValidationService = validation_service
        # add user service as direct dependency
        self._user_service: UserService = user_service

    def search(self, user_input: str) -> SearchResponse:
        """Creates a search term, fetches results, and validates relevance."""
        search_term = self._user_service.create_search_term(user_input)
        search_results = self.web_search_service.fetch_results(search_term)

        se_descriptions = [result["snippet"] for result in search_results]

        # Validate each result against the query
        validation_results: List[ValidationResult] = [
            self.validation_service.validate(search_term, result)
            for result in se_descriptions
        ]

        return {
            "search_term": search_term,
            "web_results": se_descriptions,
            "validation_results": validation_results,
            "all_results": search_results,
        }
