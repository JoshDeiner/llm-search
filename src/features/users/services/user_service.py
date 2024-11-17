
class UserService:
    def sanitize_input(self, user_input: str) -> str:
        """Sanitizes user input by stripping whitespace and converting to lowercase."""
        return user_input.strip().lower()

    def create_search_term(self, user_input: str) -> str:
        """Generates a search term based on user input."""
        sanitized_input = self.sanitize_input(user_input)
        return sanitized_input
    
    # create a method to make sure input is not empty
    def validate_input(self, user_input: str) -> bool:
        """Validates that the user input is not empty."""
        return bool(user_input)