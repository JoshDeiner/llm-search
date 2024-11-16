
from src.shared.config.constants import WEB_SEARCH_URL
from src.shared.services.search_engine_service import SearchEngineService
# from src.features.users.services.user_query_validation_service import UserService
from src.shared.services.search_prototype.web_search_pipeline import WebSearchPipeline
from typing import Any
def create_web_search_pipeline(user_service: Any) -> WebSearchPipeline:
    search_engine_service = SearchEngineService(host=WEB_SEARCH_URL, engines=["brave"])
    user_service = user_service
    return WebSearchPipeline(search_engine_service, user_service)