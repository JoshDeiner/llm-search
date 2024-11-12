
from typing import List
from typing import Dict
from typing import Union

from src.services.search_validation_service import ValidationResult

SearchEngineResults = str


SearchResponse = Dict[str, Union[str, List[Union[str, ValidationResult]]]]