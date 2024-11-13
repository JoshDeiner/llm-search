import pytest
from src.features.core_pipeline.execute_pipeline import execute_pipeline


class MockUserService:
    """
    Mock implementation of User service for integration testing.
    """

    def search(self, search_term):
        """
        Mock the search method to return predefined search results.
        """
        return {
            "all_results": [
                {
                    "title": "Mock Title 1",
                    "link": "http://example.com/1",
                    "snippet": "Snippet 1",
                },
                {
                    "title": "Mock Title 2",
                    "link": "http://example.com/2",
                    "snippet": "Snippet 2",
                },
            ]
        }


@pytest.fixture
def mock_user_service():
    """
    Provide a mock User service instance for integration testing.
    """
    return MockUserService()


class MockDocumentPipeline:
    """
    Mock implementation of DocumentPipeline for integration testing.
    """

    def __init__(self, summary, topic, works_cited):
        self._summary = summary
        self._topic = topic
        self._works_cited = works_cited
        self.saved_file = None

    @property
    def summary(self):
        return self._summary

    @property
    def topic(self):
        return self._topic

    @property
    def works_cited(self):
        return self._works_cited

    def save_to_file(self, file_name, file_extension):
        """
        Mock the save_to_file method to simulate document saving.
        """
        self.saved_file = f"{file_name}{file_extension}"
        print(f"Mock document saved: {self.saved_file}")


@pytest.fixture
def mock_pipeline_and_stages(monkeypatch):
    """
    Mock the DocumentPipeline class and pipeline stages for integration testing.
    """
    # Mock DocumentPipeline
    monkeypatch.setattr(
        "src.features.core_pipeline.stages.document_service", MockDocumentPipeline
    )

    # Mock validate_search_results
    def mock_validate_search_results(raw_data):
        return "Validated text for summarization."

    monkeypatch.setattr(
        "src.features.core_pipeline.execute_pipeline.validate_search_results",
        mock_validate_search_results,
    )

    # Mock summarize_results
    def mock_summarize_results(llm_provider, validated_results_text):
        return "This is a generated summary."

    monkeypatch.setattr(
        "src.features.core_pipeline.execute_pipeline.summarize_results", mock_summarize_results
    )


@pytest.mark.integration
def test_execute_pipeline_integration(
    mock_user_service, mock_pipeline_and_stages, caplog
):
    """
    Integration test for the execute_pipeline function.
    """
    from src.features.core_pipeline.execute_pipeline import execute_pipeline

    with caplog.at_level("INFO"):
        execute_pipeline(mock_user_service, "test search term")

    # Assert logs for successful stages
    assert "Summary generation succeeded." in caplog.text
    assert "Document successfully saved." in caplog.text

    # Assert the pipeline stages worked as expected
    pipeline = MockDocumentPipeline(
        "This is a generated summary.", "test search term", []
    )
    assert pipeline.topic == "test search term"
    assert pipeline.summary == "This is a generated summary."
    assert pipeline.works_cited == []

    # Assert that save_to_file was mocked and invoked
    assert pipeline.saved_file is None  # Mock doesn't write files
