import logging
from requests.exceptions import RequestException
from user_service.factory import get_user_service  # Import the user service factory


def execute_search(query):
    """
    Executes a search using the provided query.

    Parameters:
    query (dict): The formatted query dictionary.

    Returns:
    dict: The raw search data returned by the search engine, or None if an error occurs.
    """
    # Initialize the user service instance
    user_service = get_user_service()

    try:
        # Send the query to the search engine via user_service
        search_data = user_service.search(query)
        logging.info("Search executed successfully.")
        return search_data
    except RequestException as e:
        logging.error(f"Network error during search execution: {e}")
        return None
