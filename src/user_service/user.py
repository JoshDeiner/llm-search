# user_service/user.py

from src.services.search_term_service import SearchTermService
from src.services.web_search_service import WebSearchService

from src.services.search_validation_service import SearchValidationService
from src.services.search_validation_service import ValidationResult

from typing import List
from typing import Dict
from typing import Union

from src.shared.types import SearchEngineResults

SearchResponse = Dict[str, Union[str, List[Union[str, ValidationResult]]]]


class User:
    def __init__(
        self,
        search_term_service: SearchTermService,
        web_search_service: WebSearchService,
        validation_service: SearchValidationService,
    ) -> None:
        self.search_term_service: SearchTermService = search_term_service
        self.web_search_service: WebSearchService = web_search_service
        self.validation_service: SearchValidationService = validation_service

    def search(self, user_input: str) -> List[str]:
        """Creates a search term, fetches results, and validates relevance."""
        search_term = self.search_term_service.create_search_term(user_input)
        search_results = self.web_search_service.fetch_results(search_term)

        se_descriptions = [result['snippet'] for result in search_results]

        # Validate each result against the query
        validation_results: List[ValidationResult] = [
            self.validation_service.validate(search_term, result)
            for result in se_descriptions
        ]

        return {
            "search_term": search_term,
            "web_results": se_descriptions,
            "validation_results": validation_results,
            "all_results": search_results
        }
