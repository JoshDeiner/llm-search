# services/search_service.py

import os
import logging
from constants import WEB_SEARCH_URL
from langchain_community.utilities import SearxSearchWrapper

def init_searxng_host():
    """Initializes the SearxNG search engine host based on the environment."""

    host = WEB_SEARCH_URL
    output = 3  # Number of results to retrieve
    search = SearxSearchWrapper(searx_host=host, k=output)
    logging.info("SearxNG search engine initialized")
    return search
