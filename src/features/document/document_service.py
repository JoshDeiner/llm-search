from typing import Type
from src.features.document.document_creator import DocumentCreator

class DocumentService:
    def __init__(self, file_type: str, document_creator: Type[DocumentCreator] = DocumentCreator) -> None:
        self._file_type = self._normalize_file_type(file_type)
        self._document_creator = document_creator

    def _normalize_file_type(self, file_type: str) -> str:
        if file_type.lower() in ["markdown", "md"]:
            return "md"
        return file_type.lower()

    def create_document(self, filename: str, content: str, title: str = "") -> None:
        document_creator = self._document_creator(
            file_type=self._file_type, filename=filename, title=title, content=content
        )
        document_creator.create_document()
