import pytest
from pytest import MonkeyPatch
from typing import Generator, Dict, Any
from src.core_pipeline.execute_pipeline import execute_pipeline
from src.core_pipeline.stages.document import DocumentPipeline
from src.user_service.user import User


class MockUserService:
    """
    Mock implementation of User service for integration testing.
    """

    def search(self, search_term: str) -> Dict[str, Any]:
        """
        Mock the search method to return a predefined search result.

        :param search_term: The search term provided by the user.
        :return: A mock dictionary of search results.
        """
        return {
            "all_results": [
                {
                    "title": "Title 1",
                    "link": "http://example.com/1",
                    "snippet": "Snippet 1",
                },
                {
                    "title": "Title 2",
                    "link": "http://example.com/2",
                    "snippet": "Snippet 2",
                },
            ]
        }


@pytest.fixture
def mock_user_service(monkeypatch: MonkeyPatch) -> MockUserService:
    """
    Provide a mock User service with stubbed methods for integration testing.

    :param monkeypatch: pytest's MonkeyPatch fixture for modifying objects.
    :return: A MockUserService instance.
    """
    return MockUserService()


class MockDocumentPipeline:
    """
    Mock implementation of DocumentPipeline for integration testing.
    """

    def __init__(self, summary: str, topic: str, works_cited: list[str]) -> None:
        """
        Mock the DocumentPipeline initializer.

        :param summary: The document summary.
        :param topic: The document topic.
        :param works_cited: A list of works cited references.
        """
        self.summary = summary
        self.topic = topic
        self.works_cited = works_cited

    def save_to_file(self, file_name: str, file_extension: str) -> None:
        """
        Mock the save_to_file method to simulate document saving.

        :param file_name: Name of the file to save.
        :param file_extension: File extension to use.
        """
        print(f"Mock document saved: {file_name}{file_extension}")


@pytest.fixture
def mock_pipeline(monkeypatch: MonkeyPatch) -> None:
    """
    Mock the DocumentPipeline class to avoid file creation.

    :param monkeypatch: pytest's MonkeyPatch fixture for modifying objects.
    """
    monkeypatch.setattr(
        "src.core_pipeline.execute_pipeline.DocumentPipeline", MockDocumentPipeline
    )


@pytest.fixture
def mock_stages(monkeypatch: MonkeyPatch) -> None:
    """
    Mock the stages of the pipeline (validation, summarization).

    :param monkeypatch: pytest's MonkeyPatch fixture for modifying objects.
    """

    def mock_validate_search_results(raw_data: Dict[str, Any]) -> str:
        return "Validated text"

    def mock_summarize_results(
        llm_provider: object, validated_results_text: str
    ) -> str:
        return "Summary content"

    monkeypatch.setattr(
        "src.core_pipeline.execute_pipeline.validate_search_results",
        mock_validate_search_results,
    )
    monkeypatch.setattr(
        "src.core_pipeline.execute_pipeline.summarize_results", mock_summarize_results
    )


def test_execute_pipeline_integration(
    mock_user_service: MockUserService, mock_pipeline: None, mock_stages: None
) -> None:
    """
    Integration test for the execute_pipeline function.

    :param mock_user_service: Mocked User service instance.
    :param mock_pipeline: Mocked DocumentPipeline instance.
    :param mock_stages: Mocked pipeline stages (validation, summarization).
    """
    execute_pipeline(mock_user_service, "test search term")
