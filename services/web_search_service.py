# services/web_search_service.py

import os
import logging

from constants import WEB_SEARCH_URL
from services.search_service import init_searxng_host

class WebSearchService:
    def __init__(self, web_search_url: str = WEB_SEARCH_URL):
        self.web_search_url = web_search_url

    def fetch_results(self, search_term: str) -> list:
        ''' query search engine '''
        logging.info(f"Executing search query: {search_term}")
        search = init_searxng_host()
        r = search.run(search_term, language="en-us")

        logging.info(f"Search results: {r}")
        return r

