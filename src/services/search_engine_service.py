# services/search_service.py


import os
import logging
from src.constants import WEB_SEARCH_URL
from langchain_community.utilities import SearxSearchWrapper  # Direct import



def SearchEngineService() -> SearxSearchWrapper:
    """Initializes the SearxNG search engine host based on the environment."""
    return SearxSearchWrapper(
        searx_host=WEB_SEARCH_URL,
        k=3
    )