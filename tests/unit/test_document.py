import pytest
from src.core_pipeline.stages.document import DocumentPipeline


@pytest.fixture
def test_data():
    """
    Provide reusable test data for the pipeline.
    """
    summary = "This is a test summary.\nAnother test summary line."
    topic = "Test Topic"
    works_cited = ["Reference 1", "Reference 2"]
    pipeline = DocumentPipeline(summary=summary, topic=topic, works_cited=works_cited)
    return summary, topic, works_cited, pipeline


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
        "src.core_pipeline.stages.document.create_document"
    )

    file_name = "test_output"
    file_extension = ".md"
    pipeline.save_to_file(file_name=file_name, file_extension=file_extension)

    # Check the generated content passed to create_document
    expected_content = (
        "# Summary of Test Topic\n\n"
        "This is a test summary.\nAnother test summary line.\n\n"
        "## Works Cited\n"
        "- Reference 1\n"
        "- Reference 2\n"
    )
    mock_create_document.assert_called_once_with(
        file_name + file_extension, expected_content
    )


@pytest.mark.unit
def test_save_to_file_without_works_cited(mocker, test_data):
    """
    Test saving to file without "Works Cited".
    """
    summary, topic, _, _ = test_data
    pipeline_no_citations = DocumentPipeline(summary=summary, topic=topic)
    mock_create_document = mocker.patch(
        "src.core_pipeline.stages.document.create_document"
    )

    file_name = "test_output_no_citations"
    file_extension = ".md"
    pipeline_no_citations.save_to_file(
        file_name=file_name, file_extension=file_extension
    )

    # Check the generated content passed to create_document
    expected_content = (
        "# Summary of Test Topic\n\n"
        "This is a test summary.\nAnother test summary line.\n\n"
    )
    mock_create_document.assert_called_once_with(
        file_name + file_extension, expected_content
    )


@pytest.mark.unit
def test_save_to_file_permission_error(mocker, test_data, caplog):
    """
    Test that a PermissionError during save is handled gracefully.
    """
    _, _, _, pipeline = test_data
    mocker.patch(
        "src.core_pipeline.stages.document.create_document", side_effect=PermissionError
    )

    pipeline.save_to_file(file_name="restricted_output")

    # Verify PermissionError is logged
    assert "Permission denied" in caplog.text


@pytest.mark.unit
def test_invalid_file_extension(test_data, caplog):
    """
    Test handling of unsupported file extensions.
    """
    _, _, _, pipeline = test_data
    pipeline.save_to_file(file_name="test_output", file_extension=".exe")

    # Verify log error message
    assert "Unsupported file extension" in caplog.text
