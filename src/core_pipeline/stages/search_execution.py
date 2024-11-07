import logging
from requests.exceptions import RequestException

from src.core_pipeline.validators.result_validator import validate_search_engine_results
from src.core_pipeline.stages.data_processing import process_results
from src.user_service.user import User

from numpy import bool_
from numpy import float64

from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union


from typing import Tuple
from typing import TypeVar

NumericStrBool = Union[
    float, bool, float, str
]  # Replace numpy.float64 and numpy.bool_ with float and bool
SearchResult = Dict[str, Union[str, List[Dict[str, NumericStrBool]]]]

FetchFunction = Callable[
    ..., Optional[SearchResult]
]  # Type for functions that fetch search results

# Define a TypeVar to represent any argument types that the function may accept
T = TypeVar("T")


def fetch_web_results(
    user_service: User, search_term: str
) -> Optional[Union[SearchResult, List[str]]]:
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
        return None  # Return None to indicate network error


def validate_search_results(search_data: SearchResult) -> Optional[str]:
    """
    Validates search results and processes them for summarization.

    Parameters:
    - search_data: Raw search data fetched from the web.

    Returns:
    - Processed results text ready for summarization, or None if no valid results.
    """
    # Validate the search results
    validated_results = validate_search_engine_results(search_data)

    # Process validated results for summarization
    if not validated_results:
        logging.warning("No valid results after validation.")
        return None

    processed_text: str = process_results(validated_results)
    return processed_text


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
            return results
        else:
            logging.warning(
                f"Validation failed or network error on attempt {attempt}. Retrying..."
            )

    logging.error("All retries exhausted. Validation failed.")
    return None
