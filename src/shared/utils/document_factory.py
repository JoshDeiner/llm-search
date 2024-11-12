from src.shared.utils.create_document import DocumentCreator

class DocumentFactory:
    @staticmethod
    def create_document_creator(file_type: str, filename: str, title: str = "", content: str = ""):
        if file_type == "markdown":
            return DocumentCreator(filename, title, content)
        # Add more conditions for different file types
        else:
            raise ValueError(f"Unsupported file type: {file_type}")