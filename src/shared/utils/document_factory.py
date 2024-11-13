from src.shared.utils.create_document import DocumentCreator


class DocumentFactory:
    @staticmethod
    def create_document_creator(
        file_type: str, filename: str, title: str = "", content: str = ""
    ):
        normalized_file_type = DocumentFactory._normalize_file_type(file_type)
        if normalized_file_type == "md":
            return DocumentCreator(filename, title, content)
        # Add more conditions for different file types
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    @staticmethod
    def _normalize_file_type(file_type: str) -> str:
        if file_type == "markdown":
            return "md"
        return file_type
