import logging
import pprint
from typing import Dict
from typing import List
from typing import Union
from typing import Any


# Type aliases for readability
SearchEngineData = Dict[str, Union[str, List[Dict[str, Any]]]]

def validate_search_engine_results(
    search_data: SearchEngineData,
) -> List[Dict[str, Any]]:
    """
    Validates search engine results based on associated validation data.

    :param search_data: A dictionary containing web results and validation results.
                        - "web_results": List of search result dictionaries.
                        - "validation_results": List of validation dictionaries.
    :return: A list of validated search results. If no results are validated, return all web results.
    """
    search_engine_results = search_data.get("web_results", [])
    validation_results = search_data.get("validation_results", [])

    # Log the raw data for debugging
    logging.info("Raw search engine results:")
    logging.info(pprint.pformat(search_engine_results))
    logging.info("Raw validation results:")
    logging.info(pprint.pformat(validation_results))

    # Handle cases where validation_results is empty
    if not validation_results:
        logging.info("No validation results provided. Returning all web results.")
        return search_engine_results

    # Ensure both are lists and have matching lengths
    if not isinstance(search_engine_results, list) or not isinstance(validation_results, list):
        logging.error("Invalid input: web_results and validation_results must be lists.")
        return []

    if len(search_engine_results) != len(validation_results):
        logging.error("Mismatched lengths: web_results and validation_results must have the same length.")
        return []

    # Perform validation
    validated_results = [
        result
        for result, validation in zip(search_engine_results, validation_results)
        if isinstance(validation, dict) and validation.get("is_valid", False)
    ]

    # Return validated results, or fallback to all web results if none are validated
    return validated_results if validated_results else search_engine_results
