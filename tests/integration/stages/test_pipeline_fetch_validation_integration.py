import pytest
import logging
from src.core_pipeline.stages.search_execution import retry_with_validation
from src.core_pipeline.stages.search_execution import fetch_web_results
from src.core_pipeline.stages.search_execution import validate_search_results

from src.users.models.user import User

# Fixture for the user_service mock
@pytest.fixture
def user_service(mocker):
    # Mock the User class (you can specify methods and attributes that you expect to be called)
    mock_user_service = mocker.MagicMock(spec=User)
    return mock_user_service

@pytest.mark.integration
def test_fetch_failure(mocker, user_service, caplog):
    # Simulate a fetch failure (returns None after retries)
    mock_fetch = mocker.patch('src.core_pipeline.stages.search_execution.fetch_web_results', return_value=None)

    # Simulating the retry with validation block (steps 1 and 2)
    raw_search_data = retry_with_validation(mock_fetch, user_service, "Test Search Term")
    
    if raw_search_data is None:
        logging.error("Failed to fetch search results after retries.")
    
    # Check the logs for the correct error message indicating fetch failure
    assert "Failed to fetch search results after retries." in caplog.text
    
    # Ensure fetch was called the correct number of times (e.g., 3 times for retries)
    mock_fetch.assert_called_with(user_service, "Test Search Term")  # Ensure it's called with correct arguments
    assert mock_fetch.call_count == 3  # Expecting 3 calls for the retries


