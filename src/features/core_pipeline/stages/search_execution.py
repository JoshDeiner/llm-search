import logging
from requests.exceptions import RequestException

from src.features.core_pipeline.validators.result_validator import (
    validate_search_engine_results,
)
from src.features.users.models.user import User

from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union
from typing import Tuple
from typing import TypeVar

# Type aliases
NumericStrBool = Union[float, bool, str]
SearchResult = Dict[str, Union[str, List[Dict[str, NumericStrBool]]]]
FetchFunction = Callable[..., Optional[SearchResult]]
AllResults = List[Dict[str, Optional[str]]]  # Type alias for all_results

# Define a TypeVar to represent any argument types that the function may accept
T = TypeVar("T")


def process_results(search_results: str) -> str:
    """
    Processes raw search results for summarization, performing any necessary
    cleaning or transformations.

    Parameters:
    search_results (list): The list of search engine results to process.

    Returns:
    str: A single string with all results concatenated for summarization.
    """
    # Example: combine the results into a single string for summarization
    processed_results = "\n\n".join(search_results)
    return processed_results


def fetch_web_results(user_service: User, search_term: str) -> Optional[SearchResult]:
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
        search_data: SearchResult = user_service.search(search_term)
        return search_data
    except RequestException as e:
        logging.error(f"Network error during search execution: {e}", exc_info=True)
        return None


def validate_search_results(search_data: SearchResult) -> Optional[str]:
    """
    Validates search results and processes them for summarization.

    Parameters:
    - search_data: Raw search data fetched from the web.

    Returns:
    - Processed results text ready for summarization, or None if no valid results.
    """
    validated_results = validate_search_engine_results(search_data)

    if not validated_results:
        logging.warning("No valid results after validation.")
        return None

    processed_text: str = process_results(validated_results)
    return processed_text


def extract_works_cited(all_results: AllResults) -> List[str]:
    """
    Extracts works cited entries from search results.

    :param all_results: List of result dictionaries containing 'title', 'link', and 'snippet'.
    :return: List of formatted citation strings.
    """
    return [
        f"{entry.get('title', 'No Title')}: {entry.get('link', 'No Link') or 'No Link'}"
        for entry in all_results
        if isinstance(entry, dict) and entry.get("snippet")
    ]


def retry_with_validation(
    func: FetchFunction, *args: Tuple[T, ...], max_retries: int = 3
) -> Optional[SearchResult]:
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
            logging.debug(f"Results returned: {results}")  # Debug log
            return results
        else:
            logging.warning(
                f"Validation failed or network error on attempt {attempt}. Retrying..."
            )

    logging.error("All retries exhausted. Validation failed.")
    return None
