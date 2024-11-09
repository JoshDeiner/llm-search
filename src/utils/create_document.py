import os

def create_document(filename: str, title: str = None, content: str = "") -> None:
    """
    Creates a document with the specified title and content.
    
    :param filename: Name of the file to create.
    :param title: (Optional) The title to include in the document.
    :param content: The main content of the document.
    """
    try:
        # Ensure the directory exists, create it if missing
        directory = os.path.dirname(os.path.abspath(filename))
        if directory and not os.path.exists(directory):
            os.makedirs(directory)  # Automatically create the directory

        # Prepare the file content
        file_content = ""
        if title:
            file_content += f"# {title}\n\n"  # Add a title in Markdown format
        file_content += content

        # Write to the file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(file_content)

        print(f"Document '{filename}' created successfully.")

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
