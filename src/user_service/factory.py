from src.services.search_term_service import SearchTermService
from src.services.web_search_service import WebSearchService
from src.services.search_validation_service import SearchValidationService
from src.user_service.user import User
from src.constants import WEB_SEARCH_URL


def get_user_service() -> User:
    """Factory function to instantiate User with dependencies injected."""
    # Dynamically fetch URL, defaulting to port 8080
    search_term_service = SearchTermService()
    web_search_service = WebSearchService(web_search_url=WEB_SEARCH_URL)
    validation_service = SearchValidationService()

    # Pass all services to the User instance
    return User(search_term_service, web_search_service, validation_service)
