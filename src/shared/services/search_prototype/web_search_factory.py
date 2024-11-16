
from src.shared.config.constants import WEB_SEARCH_URL
from src.shared.services.search_engine_service import SearchEngineService
from src.features.users.user_service import UserService
from src.shared.services.search_prototype.web_search_pipeline import WebSearchPipeline

def create_web_search_pipeline() -> WebSearchPipeline:
    search_engine_service = SearchEngineService(host=WEB_SEARCH_URL, engines=["brave"])
    user_service = UserService()
    return WebSearchPipeline(search_engine_service, user_service)