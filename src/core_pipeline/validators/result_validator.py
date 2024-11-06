import logging
import pprint

from typing import Dict
from typing import List
from typing import Union

# Type aliases for readability
ValidationResult = Dict[str, Union[float, bool, str]]
WebResultsType = List[ValidationResult]
SearchData = Dict[str, Union[str, WebResultsType]]


# is this right?

"""
Strict Filtering: If the caller should only receive validated results, then Option 1 (returning validated_se_results only) is the cleanest approach.
Explicit Failure: If it’s important to signal a failure, Option 2 (returning None on full validation failure) makes the validation outcome more explicit.
Fallback Results: If you need to guarantee results regardless of validation, then keeping Option 3 (current behavior) might be best.
"""


def validate_se_results(search_data: SearchData) -> WebResultsType:
    web_results: WebResultsType = search_data.get("web_results", [])
    se_validation_results: WebResultsType = search_data.get("validation_results", [])

    logging.info("Raw web search results:")
    logging.info(pprint.pformat(web_results))

    validated_se_results = [
        result
        for result, validation in zip(web_results, se_validation_results)
        if validation.get("is_valid", False)
    ]

    return validated_se_results if validated_se_results else web_results
