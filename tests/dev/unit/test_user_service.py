import pytest
from src.features.users.services.user_query_validation_service import UserService

@pytest.fixture
def user_service() -> UserService:
    return UserService()

def test_sanitize_input(user_service: UserService) -> None:
    # Act
    sanitized_input = user_service.sanitize_input("  Hello World  ")

    # Assert
    assert sanitized_input == "hello world"

def test_create_search_term(user_service: UserService) -> None:
    # Act
    search_term = user_service.create_search_term("  Hello World  ")

    # Assert
    assert search_term == "hello world"