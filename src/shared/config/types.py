from typing import List
from typing import Dict
from typing import Union

from typing import TypedDict

from src.shared.services.search_validation_service import ValidationResult

SearchEngineResults = str


SearchResponse = Dict[str, Union[str, List[Union[str, ValidationResult]]]]


class SearchResult(TypedDict):
    snippet: str
    title: str
    link: str
    engines: List[str]
    category: str
