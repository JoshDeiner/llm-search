from typing import List
import logging
from src.utils.create_document import create_document


class DocumentPipeline:
    """
    A service class to manage document creation from provided summaries.
    This includes managing summaries, generating titles, and saving content to a text file.
    """

    def __init__(self, summary: str, topic: str, works_cited: List[str] = []):
        """
        Initialize the pipeline with a summary string, a topic, and optional works cited references.

        :param summary: A string summary provided to the pipeline.
        :param topic: The main topic of the document.
        :param works_cited: Optional list of works cited references.
        """
        self._summary = summary
        self._topic = topic
        self._title = f"Summary of {topic}"
        self._works_cited = works_cited or []

    @property
    def summary(self) -> str:
        """Getter for the summary attribute."""
        return self._summary

    @property
    def title(self) -> str:
        """Getter for the title attribute."""
        return self._title

    def save_to_file(
        self, file_name: str = "output", file_extension: str = ".md"
    ) -> None:
        """
        Saves the generated document content to a text file, organized by sections.

        The document includes:
        - Title (header)
        - Summary section
        - Optional "Works Cited" section (if works_cited is provided)

        :param file_name: Name of the file to save (without extension).
        :param file_extension: File extension (default is ".md").
        """
        # Prepare content sections
        title_section = f"# {self._title}\n\n"
        summary_section = self._summary + "\n\n"

        # Only add works cited section if there's content
        works_cited_section = ""
        if self._works_cited:
            works_cited_section = (
                "## Works Cited\n"
                + "\n".join(f"- {item}" for item in self._works_cited)
                + "\n"
            )

        # Combine all sections
        document_content = title_section + summary_section + works_cited_section

        # Validate file name
        full_file_name = file_name + file_extension
        if not full_file_name.endswith((".md", ".txt")):
            logging.error(f"Unsupported file extension: {file_extension}")
            return

        # Try to save the document using create_document utility
        try:
            create_document(
                full_file_name, document_content
            )  # Pass content to utility function
            print(f"Document saved to {full_file_name}")
        except PermissionError:
            logging.error(f"Permission denied: Cannot write to file {full_file_name}")
        except IOError as e:
            logging.error(f"IO error occurred: {e}")
        except Exception as e:
            logging.error("Document creation failed", exc_info=True)
