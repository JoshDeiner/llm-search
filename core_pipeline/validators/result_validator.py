import logging
import pprint
from numpy import bool, float64
from typing import Dict, List, Union


def validate_se_results(search_data: Dict[str, Union[str, List[Dict[str, Union[float64, bool, float, str]]]]]) -> str:
    web_results = search_data.get("web_results", [])
    se_validation_results = search_data.get("validation_results", [])

    logging.info("Raw web search results:")
    logging.info(pprint.pformat(web_results))

    validated_se_results = [
        result
        for result, validation in zip(web_results, se_validation_results)
        if validation.get("is_valid", False)
    ]

    return validated_se_results if validated_se_results else web_results
