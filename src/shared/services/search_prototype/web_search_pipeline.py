
import logging
from typing import List
from src.shared.config.types import SearchResult
from src.shared.services.search_engine_service import SearchEngineService
from src.features.users.user_service import UserService

class WebSearchPipeline:
    def __init__(self, search_engine_service: SearchEngineService, user_service: UserService, search_term: str) -> None:
        self._search_engine_service = search_engine_service
        self._user_service = user_service
        self._search_term = search_term

    def main(self) -> List[SearchResult]:

        # execute steps of the pipeline

        ## step 1: create search term
        search_term = self._user_service.create_search_term(self._search_term)
        logging.info(f"Executing search query: {search_term}")
        ## add validator is search term meeting the threshold
        ## else go back up

        return self._search_engine_service.run(search_term)
    






