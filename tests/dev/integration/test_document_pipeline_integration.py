import pytest
from src.features.document.document_pipeline import DocumentPipeline

@pytest.fixture
def document_pipeline():
    summary = "This is a test summary."
    topic = "Test Topic"
    file_type = "md"
    works_cited = ["Reference 1", "Reference 2"]
    return DocumentPipeline(summary=summary, topic=topic, file_type=file_type, works_cited=works_cited)

@pytest.mark.integration
def test_save_to_file_integration(fs, document_pipeline):
    # Act
    document_pipeline.save_to_file(file_name="test_output", file_extension=".md")

    # Assert
    with open("test_output.md", "r") as file:
        content = file.read()
        assert "# Summary of Test Topic" in content
        assert "This is a test summary." in content
        assert "## Works Cited" in content
        assert "- Reference 1" in content
        assert "- Reference 2" in content