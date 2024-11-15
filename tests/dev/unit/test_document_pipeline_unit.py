import pytest
from src.features.document.document_pipeline import DocumentPipeline


class FakeDocumentService:
    """
    A fake implementation of DocumentService for testing purposes.
    Tracks created documents in memory and supports error simulation.
    """

    def __init__(self):
        self.created_documents = []
        self.raise_error = None

    def create_document(self, filename, content, title):
        if self.raise_error:
            raise self.raise_error
        self.created_documents.append({
            "filename": filename,
            "content": content,
            "title": title
        })


@pytest.fixture
def fake_document_service():
    return FakeDocumentService()


@pytest.fixture
def document_pipeline(fake_document_service):
    return DocumentPipeline(
        summary="This is a test summary.",
        topic="Test Topic",
        file_type="md",
        works_cited=["Reference 1", "Reference 2"],
        document_service=fake_document_service,
    )


@pytest.mark.unit
def test_save_to_file(document_pipeline, fake_document_service):
    # Act
    document_pipeline.save_to_file(file_name="test_output", file_extension=".md")

    # Assert
    assert len(fake_document_service.created_documents) == 1
    created_doc = fake_document_service.created_documents[0]
    assert created_doc["filename"] == "test_output.md"
    assert created_doc["title"] == "Summary of Test Topic"
    assert created_doc["content"] == (
        "# Summary of Test Topic\n\n"
        "This is a test summary.\n\n"
        "## Works Cited\n"
        "- Reference 1\n"
        "- Reference 2\n"
    )


@pytest.mark.unit
def test_save_to_file_permission_error(document_pipeline, fake_document_service):
    # Arrange
    fake_document_service.raise_error = PermissionError()

    # Act & Assert
    with pytest.raises(PermissionError) as exc_info:
        document_pipeline.save_to_file(file_name="test_output", file_extension=".md")
    
    # Check exception message explicitly
    assert "You do not have permission to save this file" in str(exc_info.value)


@pytest.mark.unit
def test_save_to_file_io_error(document_pipeline, fake_document_service):
    # Arrange
    fake_document_service.raise_error = OSError("Disk full")

    # Act & Assert
    with pytest.raises(OSError, match="Disk full"):
        document_pipeline.save_to_file(file_name="test_output", file_extension=".md")


@pytest.mark.unit
def test_save_to_file_unsupported_extension(document_pipeline):
    # Act & Assert
    with pytest.raises(ValueError, match="Unsupported file extension: .xyz"):
        document_pipeline.save_to_file(file_name="test_output", file_extension=".xyz")