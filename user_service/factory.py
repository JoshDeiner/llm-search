# user_service/factory.py

from services.search_term_service import SearchTermService
from services.web_search_service import WebSearchService

from user_service.user import User
from constants import WEB_SEARCH_URL

def get_user_service() -> User:
    """Factory function to instantiate User with dependencies injected."""
    # Dynamically fetch URL, defaulting to port 8080
    search_term_service = SearchTermService()
    web_search_service = WebSearchService(web_search_url=WEB_SEARCH_URL)
    return User(search_term_service, web_search_service)

