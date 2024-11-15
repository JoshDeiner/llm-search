
import pytest
from src.features.core_pipeline.execute_pipeline import execute_pipeline
from src.features.users.models.user import User

@pytest.fixture
def mock_user_service(mocker):
    return mocker.MagicMock(spec=User)

@pytest.fixture
def search_term():
    return "test search term"

@pytest.mark.unit
def test_execute_pipeline(mocker, mock_user_service, search_term):
    # Arrange
    mock_llm_provider = mocker.patch('src.features.core_pipeline.execute_pipeline.LLMProvider')
    mock_retry_with_validation = mocker.patch('src.features.core_pipeline.execute_pipeline.retry_with_validation')
    mock_validate_search_results = mocker.patch('src.features.core_pipeline.execute_pipeline.validate_search_results')
    mock_summarize_results = mocker.patch('src.features.core_pipeline.execute_pipeline.summarize_results')
    mock_document_pipeline = mocker.patch('src.features.core_pipeline.execute_pipeline.DocumentPipeline')

    mock_llm_provider.return_value = mocker.MagicMock()
    mock_retry_with_validation.return_value = {"all_results": [{"title": "Test Title", "link": "http://example.com"}]}
    mock_validate_search_results.return_value = "Validated results text"
    mock_summarize_results.return_value = "This is a test summary."
    mock_document_pipeline.return_value.save_to_file = mocker.MagicMock()

    # Act
    execute_pipeline(mock_user_service, search_term)

    # Assert
    mock_document_pipeline.return_value.save_to_file.assert_called_once_with(
        file_name="pipeline_output", file_extension=".md"
    )

@pytest.mark.unit
def test_execute_pipeline_no_results(mocker, mock_user_service, search_term):
    # Arrange: Mock the retry_with_validation function to simulate no results being fetched
    mock_retry_with_validation = mocker.patch('src.features.core_pipeline.execute_pipeline.retry_with_validation')
    mock_retry_with_validation.return_value = None

    # Act & Assert: Ensure that execute_pipeline raises a ValueError when no results are fetched
    with pytest.raises(ValueError, match="Failed to fetch search results after retries."):
        execute_pipeline(mock_user_service, search_term)

@pytest.mark.unit
def test_execute_pipeline_summary_failure(mocker, mock_user_service, search_term):
    # Arrange
    mock_llm_provider = mocker.patch('src.features.core_pipeline.execute_pipeline.LLMProvider')
    mock_retry_with_validation = mocker.patch('src.features.core_pipeline.execute_pipeline.retry_with_validation')
    mock_validate_search_results = mocker.patch('src.features.core_pipeline.execute_pipeline.validate_search_results')
    mock_summarize_results = mocker.patch('src.features.core_pipeline.execute_pipeline.summarize_results')

    mock_llm_provider.return_value = mocker.MagicMock()
    mock_retry_with_validation.return_value = {"all_results": [{"title": "Test Title", "link": "http://example.com"}]}
    mock_validate_search_results.return_value = "Validated results text"
    mock_summarize_results.return_value = None

    # Act & Assert
    with pytest.raises(ValueError, match="Summary generation failed."):
        execute_pipeline(mock_user_service, search_term)