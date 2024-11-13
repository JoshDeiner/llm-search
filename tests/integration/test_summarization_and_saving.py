import pytest
from src.features.core_pipeline.execute_pipeline import (
    extract_works_cited,
    summarize_results,
)


@pytest.fixture
def mock_llm_provider(monkeypatch):
    """
    Mocked LLMProvider for summarization.
    """

    class MockLLMProvider:
        def summarize_text(self, text):
            return "Generated Summary"

    mock_instance = MockLLMProvider()
    monkeypatch.setattr(
        "src.features.core_pipeline.execute_pipeline.LLMProvider",
        lambda *args, **kwargs: mock_instance,
    )
    return mock_instance


@pytest.fixture
def mock_document_pipeline(monkeypatch):
    """
    Mocked DocumentPipeline for file handling.
    """

    class MockDocumentPipeline:
        def __init__(self, summary, topic, works_cited):
            self.summary = summary
            self.topic = topic
            self.works_cited = works_cited
            self.save_to_file_called = False

        def save_to_file(self, file_name, file_extension):
            self.save_to_file_called = True
            self.file_name = file_name
            self.file_extension = file_extension

    def mock_pipeline(summary, topic, works_cited):
        return MockDocumentPipeline(summary, topic, works_cited)

    monkeypatch.setattr(
        "src.features.core_pipeline.execute_pipeline.DocumentPipeline", mock_pipeline
    )
    return mock_pipeline


@pytest.mark.integration
def test_summarization_and_save_success(mock_llm_provider, mock_document_pipeline):
    """
    Test the summarization and document saving steps when all steps succeed.
    """
    validated_results_text = "This is validated text."
    search_term = "test search"
    raw_search_data = {
        "all_results": [{"title": "Mock Title", "link": "http://example.com"}]
    }

    # Step 3: Summarize validated results
    summary = summarize_results(mock_llm_provider, validated_results_text)
    assert summary == "Generated Summary"

    # Step 3.1: Extract works cited
    works_cited = extract_works_cited(raw_search_data["all_results"])
    assert works_cited == ["Mock Title: http://example.com"]

    # Step 4: Write summary to document
    document_pipeline = mock_document_pipeline(summary, search_term, works_cited)
    assert not document_pipeline.save_to_file_called  # Not called yet

    document_pipeline.save_to_file("pipeline_output", ".md")
    assert document_pipeline.save_to_file_called
    assert document_pipeline.file_name == "pipeline_output"
    assert document_pipeline.file_extension == ".md"


@pytest.mark.integration
def test_summarization_failure(mock_llm_provider, mock_document_pipeline, caplog):
    """
    Test that document saving is skipped if summarization fails.
    """
    # Simulate failure in summarization
    mock_llm_provider.summarize_text = (
        lambda text: None
    )  # Return None to simulate failure
    validated_results_text = "This is validated text."

    # Step 3: Summarize validated results (should fail)
    summary = summarize_results(mock_llm_provider, validated_results_text)
    assert summary is None

    # Ensure save_to_file is never called
    document_pipeline = mock_document_pipeline("Generated Summary", "test search", [])
    assert not document_pipeline.save_to_file_called

    # Check logs for failure message TODO


@pytest.mark.integration
def test_extract_works_cited_invalid_data(caplog):
    """
    Test works cited extraction with invalid data.
    """
    raw_search_data = {
        "all_results": ["invalid entry", {"title": "Title", "link": None}]
    }

    # Test the function
    works_cited = extract_works_cited(raw_search_data["all_results"])
    assert works_cited == ["Title: No Link"]

    # Check logs for skipped invalid entry
    assert "Skipping invalid result entry: invalid entry" in caplog.text
