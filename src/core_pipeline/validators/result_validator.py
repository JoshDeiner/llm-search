import logging
import pprint

from typing import Dict
from typing import List
from typing import Union, Any

from src.shared.types import SearchEngineResults

# Type aliases for readability
SEValidationResult = Dict[str, Union[float, bool, str]]
SearchEngineData = Dict[str, Union[str, List[str]]]



# figure out how to define SearchEngineData
# SearchEngineResults = str
def validate_search_engine_results(
    search_data: SearchEngineData,
) -> Any:
    search_engine_results: Union[str, List[str]] = search_data.get("web_results", [])
    validation_results: Union[str, List[str]] = search_data.get("validation_results", [])

    logging.info("Raw search engine results:")
    logging.info(pprint.pformat(search_engine_results))

    validated_results = [
        result
        for result, validation in zip(search_engine_results, validation_results)
        if validation.get("is_valid", False)
    ]

    return validated_results if validated_results else search_engine_results
