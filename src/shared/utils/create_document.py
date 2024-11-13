import os


class DocumentCreator:
    def __init__(self, filename: str, title: str = "", content: str = ""):
        self.filename = filename
        self.title = title
        self.content = content

    def create_document(self) -> None:
        """
        Creates a document with the specified title and content.
        """
        try:
            # Ensure the directory exists, create it if missing
            directory = os.path.dirname(os.path.abspath(self.filename))
            if directory and not os.path.exists(directory):
                os.makedirs(directory)  # Automatically create the directory

            # Prepare the file content
            file_content = ""
            if self.title:
                file_content += f"# {self.title}\n\n"  # Add a title in Markdown format
            file_content += self.content

            # Write to the file
            with open(self.filename, "w", encoding="utf-8") as file:
                file.write(file_content)

            print(f"Document '{self.filename}' created successfully.")

        except ValueError as ve:
            # Handle value errors (e.g., invalid file content)
            print(f"A ValueError occurred: {ve}")
            raise  # Re-raise the exception for further handling

        except PermissionError as pe:
            # Handle permission errors
            print(f"A PermissionError occurred: {pe}")
            raise  # Re-raise the exception for further handling

        except Exception as e:
            # Handle all other unexpected exceptions
            print(f"An unexpected error occurred: {e}")
            raise  # Re-raise the exception for further handling
