from src.shared.services.web_search_service import WebSearchService
from src.shared.services.search_validation_service import SearchValidationService
from src.users.models.user import User
from src.constants import WEB_SEARCH_URL


def create_user_service() -> User:
    """Factory function to instantiate User with dependencies injected."""
    # Dynamically fetch URL, defaulting to port 8080
    web_search_service = WebSearchService(web_search_url=WEB_SEARCH_URL)
    validation_service = SearchValidationService()

    # Pass all services to the User instance
    return User(web_search_service, validation_service)
