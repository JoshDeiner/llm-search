import json
import logging
from constants import WEB_SEARCH_URL
from langchain_community.utilities import SearxSearchWrapper


class SearchEngineClient:
    """
    A client for interacting with the SearxNG search engine.
    """

    def __init__(self):
        """
        Initializes the search engine client.
        """
        self.search = SearxSearchWrapper(searx_host=WEB_SEARCH_URL, k=3)
        logging.info("SearxNG search engine client initialized")

    def fetch_results(self, query):
        """
        Executes a search using the provided query and returns structured results.

        Parameters:
        query (str): The search term.

        Returns:
        dict: A dictionary containing search results, or None if an error occurs.
        """
        try:
            # Replace `.run()` with the actual method for querying if necessary
            results = self.search.run(query)  # Adjust method as needed
            logging.info("Search executed successfully.")

            # Attempt to parse the results as JSON if they're not already structured
            if isinstance(results, str):
                results = json.loads(results)  # Parse JSON if results are a JSON string

            return results
        except json.JSONDecodeError:
            logging.error("Failed to parse search results as JSON.")
            return None
        except Exception as e:
            logging.error(f"Error during search execution: {e}")
            return None
