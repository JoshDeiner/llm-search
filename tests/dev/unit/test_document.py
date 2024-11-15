import pytest
from typing import Type
from src.features.document.shared import (
    DocumentPipeline,
    DocumentCreator
)
from src.features.document.document_creator import DocumentCreator

@pytest.fixture
def test_data():
    """
    Provide reusable test data for the pipeline.
    """
    summary = "This is a test summary.\nAnother test summary line."
    topic = "Test Topic"
    works_cited = ["Reference 1", "Reference 2"]
    pipeline = DocumentPipeline(
        summary=summary, topic=topic, file_type="md", works_cited=works_cited
    )
    return summary, topic, works_cited, pipeline

@pytest.fixture
def document_creator() -> Type[DocumentCreator]:
    return DocumentCreator


@pytest.mark.unit
def test_title_generation(test_data):
    """
    Test that the title is correctly generated based on the topic.
    """
    _, topic, _, pipeline = test_data
    expected_title = f"Summary of {topic}"
    assert pipeline.title == expected_title


@pytest.mark.unit
def test_summary_property(test_data):
    """
    Test that the summary property returns the correct summary string.
    """
    summary, _, _, pipeline = test_data
    assert pipeline.summary == summary


@pytest.mark.unit
def test_save_to_file_with_works_cited(mocker, test_data):
    """
    Test saving to file with "Works Cited" included.
    """
    _, _, _, pipeline = test_data
    mock_create_document = mocker.patch(
        "src.features.document.document_service.DocumentService.create_document"
    )

    file_name = "test_output"
    file_extension = ".md"
    pipeline.save_to_file(file_name=file_name, file_extension=file_extension)

    mock_create_document.assert_called_once()


@pytest.mark.unit
def test_save_to_file_without_works_cited(mocker, test_data):
    """
    Test saving to file without "Works Cited".
    """
    summary, topic, _, _ = test_data
    pipeline_no_citations = DocumentPipeline(
        summary=summary, topic=topic, file_type="md"
    )
    mock_create_document = mocker.patch(
        "src.features.document.document_service.DocumentService.create_document"
    )

    file_name = "test_output_no_citations"
    file_extension = ".md"
    pipeline_no_citations.save_to_file(
        file_name=file_name, file_extension=file_extension
    )

    mock_create_document.assert_called_once()


@pytest.mark.unit
def test_file_type_normalization():
    """
    Test that file type normalization works correctly.
    """
    pipeline = DocumentPipeline(summary="Test", topic="Test", file_type="markdown")
    assert (
        pipeline._document_service._file_type == "md"
    ), "File type normalization failed for 'markdown'."

    pipeline = DocumentPipeline(summary="Test", topic="Test", file_type="md")
    assert (
        pipeline._document_service._file_type == "md"
    ), "File type normalization failed for 'md'."

