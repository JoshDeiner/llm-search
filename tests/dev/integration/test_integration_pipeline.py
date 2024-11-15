import pytest
from src.features.core_pipeline.execute_pipeline import execute_pipeline
from src.features.users.models.user import User
from src.shared.services.web_search_service import WebSearchService
from src.shared.services.search_validation_service import SearchValidationService

@pytest.fixture
def search_term():
    return "integration test search term"

@pytest.fixture
def web_search_service():
    return WebSearchService()

@pytest.fixture
def validation_service():
    return SearchValidationService()

@pytest.fixture
def user_service(web_search_service, validation_service):
    return User(web_search_service=web_search_service, validation_service=validation_service)

@pytest.mark.integration
def test_execute_pipeline_integration(search_term, user_service):
    # Act
    execute_pipeline(user_service, search_term)

    # Assert
    with open("pipeline_output.md", "r") as file:
        content = file.read()
        assert "# Summary of integration test search term" in content
        assert "## Works Cited" in content