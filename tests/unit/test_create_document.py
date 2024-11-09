import os
import pytest
from src.utils.create_document import create_document


def test_create_document_with_title_and_content(tmp_path):
    """
    Test create_document successfully writes a document with title and content.
    """
    # Arrange
    file_path = tmp_path / "output.md"
    title = "Test Title"
    content = "This is the test content of the document."

    # Act
    create_document(filename=str(file_path), title=title, content=content)

    # Assert
    assert file_path.exists(), "File was not created."
    with open(file_path, "r", encoding="utf-8") as f:
        written_content = f.read()
    expected_content = f"# {title}\n\n{content}"
    assert (
        written_content == expected_content
    ), "File content does not match the expected output."


def test_create_document_without_title(tmp_path):
    """
    Test create_document successfully writes a document with content but no title.
    """
    # Arrange
    file_path = tmp_path / "output_no_title.md"
    content = "This is the test content of the document without a title."

    # Act
    create_document(filename=str(file_path), content=content)

    # Assert
    assert file_path.exists(), "File was not created."
    with open(file_path, "r", encoding="utf-8") as f:
        written_content = f.read()
    expected_content = content
    assert (
        written_content == expected_content
    ), "File content does not match the expected output."


# def test_create_document_creates_missing_directories(tmp_path):
#     """
#     Test create_document automatically creates missing directories.
#     """
#     # Arrange
#     nested_path = tmp_path / "nested" / "output.md"
#     title = "Test Title"
#     content = "This is the test content."

#     # Act
#     create_document(filename=str(nested_path), title=title, content=content)

#     # Assert
#     assert nested_path.exists(), "File was not created in the nested directory."
#     with open(nested_path, "r", encoding="utf-8") as f:
#         written_content = f.read()
#     expected_content = f"# {title}\n\n{content}"
#     assert written_content == expected_content, "File content does not match the expected output."


def test_create_document_creates_missing_directories(tmp_path):
    """
    Test create_document automatically creates missing directories.
    """
    # Arrange
    nested_path = tmp_path / "nonexistent_subdir" / "output.md"
    title = "Test Title"
    content = "This is the test content."

    # Ensure the directory doesn't exist initially
    assert (
        not nested_path.parent.exists()
    ), "Test setup failed: Directory unexpectedly exists."

    # Act
    create_document(filename=str(nested_path), title=title, content=content)

    # Assert
    # Verify the directory and file were created
    assert nested_path.exists(), "File was not created in the nested directory."
    with open(nested_path, "r", encoding="utf-8") as f:
        written_content = f.read()
    expected_content = f"# {title}\n\n{content}"
    assert (
        written_content == expected_content
    ), "File content does not match the expected output."


def test_create_document_permission_error(mocker, tmp_path):
    """
    Test create_document raises PermissionError when writing to a restricted location.
    """
    # Arrange
    restricted_path = tmp_path / "restricted_output.md"
    mock_open = mocker.patch("builtins.open", side_effect=PermissionError)

    # Act & Assert
    with pytest.raises(PermissionError):
        create_document(
            filename=str(restricted_path),
            title="Restricted Title",
            content="Restricted Content",
        )

    # Assert the mock was called
    mock_open.assert_called_once_with(str(restricted_path), "w", encoding="utf-8")