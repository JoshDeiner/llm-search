import logging
from requests.exceptions import RequestException

from src.core_pipeline.validators.result_validator import validate_se_results
from src.core_pipeline.stages.data_processing import (
    process_results,
)
from src.user_service.user import User

from numpy import bool
from numpy import float64

from typing import Callable
from typing import Dict
from typing import List
from typing import Union


def fetch_web_results(
    user_service: User, search_term: str
) -> Dict[str, Union[str, List[Dict[str, Union[float64, bool, float, str]]]]]:
    """
    Fetches raw web search results without validation.

    Parameters:
    - user_service: The service handling the search operation.
    - search_term: The search term to query.

    Returns:
    - Raw search data or None if a network error occurs.
    """
    try:
        # Perform the search
        search_data = user_service.search(search_term)
        logging.info("search_data", search_data)
        logging.info(f"search_data: {search_data}")

        return search_data
    except RequestException as e:
        logging.error(f"Network error during search execution: {e}")
        return None  # Return None to indicate network error


def validate_search_results(
    search_data: Dict[
        str, Union[str, List[Dict[str, Union[float64, bool, float, str]]]]
    ]
) -> str:
    """
    Validates search results and processes them for summarization.

    Parameters:
    - search_data: Raw search data fetched from the web.

    Returns:
    - Processed results text ready for summarization, or None if no valid results.
    """
    # Validate the search results
    validated_results = validate_se_results(search_data)

    # Process validated results for summarization
    if not validated_results:
        logging.warning("No valid results after validation.")
        return None

    processed_text = process_results(validated_results)
    return processed_text


def retry_with_validation(
    func: Callable, *args, max_retries=3
) -> Dict[str, Union[str, List[Dict[str, Union[float64, bool, float, str]]]]]:
    """
    Attempts to execute a function with validation, retrying if necessary.

    Parameters:
    - func: The function to execute.
    - *args: Arguments to pass to the function.
    - max_retries: The maximum number of retries.

    Returns:
    - The result of the function if successful, or None if retries are exhausted.
    """
    for attempt in range(1, max_retries + 1):
        logging.info(f"Attempt {attempt} of {max_retries}")

        results = func(*args)
        if results and "No results found" not in results:
            logging.info("Validation succeeded.")
            return results
        else:
            logging.warning("Validation failed or network error. Retrying...")

    logging.error("All retries exhausted. Validation failed.")
    return None
