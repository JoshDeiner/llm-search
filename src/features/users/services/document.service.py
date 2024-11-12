# document_service.py

import os


class DocumentService:
    def __init__(self):
        self.documents = (
            {}
        )  # In-memory storage for demo purposes (consider using a database)

    def create_document(self, user_service, user_id, filename, title, content):
        """Creates a document and associates it with a user."""
        if not user_service.user_exists(user_id):
            print(f"User {user_id} does not exist. Document creation failed.")
            return

        try:
            with open(filename, "w") as file:
                file.write(f"# {title}\n\n")  # Adding a title with Markdown format
                file.write(content)
            self.documents[filename] = user_id  # Registering document ownership
            print(f'Document "{filename}" created successfully by {user_id}.')
        except Exception as e:
            print(f"An error occurred while creating the document: {e}")

    def get_document(self, filename):
        """Retrieves the content of a document."""
        if filename in self.documents:
            try:
                with open(filename, "r") as file:
                    content = file.read()
                return content
            except Exception as e:
                print(f"An error occurred while reading the document: {e}")
                return None
        else:
            print(f'Document "{filename}" not found.')
            return None

    def delete_document(self, user_service, user_id, filename):
        """Deletes a document if the user has the right permissions."""
        if filename not in self.documents:
            print(f'Document "{filename}" does not exist.')
            return

        if self.documents[filename] != user_id:
            print(f"User {user_id} does not have permission to delete this document.")
            return

        try:
            os.remove(filename)
            del self.documents[filename]  # Remove document from in-memory tracking
            print(f'Document "{filename}" deleted successfully by {user_id}.')
        except Exception as e:
            print(f"An error occurred while deleting the document: {e}")


# Example usage
if __name__ == "__main__":
    # Simulating UserService for demonstration
    class UserService:
        def __init__(self):
            self.users = {}

        def add_user(self, user_id, user_info):
            self.users[user_id] = user_info
            print(f"User {user_id} added.")

        def user_exists(self, user_id):
            return user_id in self.users

    # Example usage of DocumentService
    user_service = UserService()
    user_service.add_user("user1", {"name": "Alice"})

    document_service = DocumentService()
    document_service.create_document(
        user_service,
        "user1",
        "news_report.md",
        "Breaking News",
        "This is a sample news report.",
    )

    # Retrieve and print the document
    content = document_service.get_document("news_report.md")
    print(content)

    # Delete the document
    document_service.delete_document(user_service, "user1", "news_report.md")
