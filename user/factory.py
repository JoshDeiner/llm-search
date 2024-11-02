# user_service/factory.py

from services.search_term_service import SearchTermService
from services.web_search_service import WebSearchService
from user_service.user import User


def get_user_service(web_search_url: str) -> User:
    """Factory function to instantiate User with dependencies injected."""
    search_term_service = SearchTermService()
    web_search_service = WebSearchService(web_search_url=web_search_url)
    return User(search_term_service, web_search_service)
