import pytest
from src.features.document.shared import DocumentCreator

@pytest.mark.unit
def test_create_document_with_title():
    """
    Test creating a document with a title.
    """
    creator = DocumentCreator(file_type="md", filename="test.md", title="Test Title", content="Test content.")
    creator.create_document()
    # Add assertions to verify the document creation if necessary

@pytest.mark.unit
def test_create_document_without_title():
    """
    Test creating a document without a title.
    """
    creator = DocumentCreator(file_type="md", filename="test.md", content="Test content.")
    creator.create_document()
    # Add assertions to verify the document creation if necessary

@pytest.mark.unit
def test_create_document_invalid_file_type():
    """
    Test creating a document with an invalid file type.
    """
    with pytest.raises(ValueError, match="Unsupported file type: txt"):
        DocumentCreator(file_type="txt", filename="test.txt", content="Test content.")

@pytest.mark.unit
def test_create_document_permission_error(mocker):
    """
    Test handling of PermissionError during document creation.
    """
    creator = DocumentCreator(file_type="md", filename="test.md", content="Test content.")
    mocker.patch("builtins.open", side_effect=PermissionError)
    with pytest.raises(PermissionError):
        creator.create_document()

@pytest.mark.unit
def test_create_document_unexpected_error(mocker):
    """
    Test handling of unexpected errors during document creation.
    """
    creator = DocumentCreator(file_type="md", filename="test.md", content="Test content.")
    mocker.patch("builtins.open", side_effect=Exception("Unexpected error"))
    with pytest.raises(Exception, match="Unexpected error"):
        creator.create_document()
