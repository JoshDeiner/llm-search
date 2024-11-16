from src.shared.services.web_search_service import WebSearchService
from src.shared.services.search_validation_service import SearchValidationService
from src.features.users.models.user import User
from src.shared.config.constants import WEB_SEARCH_URL
from typing import Any
from src.features.users.services.user_service import UserService

def create_user_service() -> User:
    """Factory function to instantiate User with dependencies injected."""
    # Dynamically fetch URL, defaulting to port 8080
    web_search_service = WebSearchService(web_search_url=WEB_SEARCH_URL)
    validation_service = SearchValidationService()
    # add user service as direct dependency
    user_service = UserService()

    # Pass all services to the User instance
    return User(web_search_service, validation_service, user_service=user_service)
