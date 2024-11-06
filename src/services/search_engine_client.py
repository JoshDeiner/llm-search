import json
import logging
from typing import Optional
from typing import Dict
from typing import Any
from typing import Union
from typing import List

from langchain_community.utilities import SearxSearchWrapper
from src.constants import WEB_SEARCH_URL


## not being used ##

SearchEngineClientResults = Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]


class SearchEngineClient:
    """
    A client for interacting with the SearxNG search engine.
    """

    def __init__(self) -> None:
        """
        Initializes the search engine client.
        """
        self.search = SearxSearchWrapper(searx_host=WEB_SEARCH_URL, k=3)
        logging.info("SearxNG search engine client initialized")

    def fetch_results(self, query: str) -> SearchEngineClientResults:
        """
        Executes a search using the provided query and returns structured results.

        Parameters:
        - query: The search term.

        Returns:
        - A dictionary or list of dictionaries containing search results, or None if an error occurs.
        """
        try:
            # Execute the search
            results = self.search.run(query)
            logging.info("Search executed successfully.")

            # Attempt to parse results as JSON if needed
            if isinstance(results, str):
                results = json.loads(
                    results
                )  # Parse JSON if results are in string format

            # Ensure results are either a dictionary or list of dictionaries
            if isinstance(results, (dict, list)):
                return results
            else:
                logging.error("Unexpected results format.")
                return None
        except json.JSONDecodeError:
            logging.error("Failed to parse search results as JSON.")
            return None
        except Exception as e:
            logging.error(f"Error during search execution: {e}")
            return None
