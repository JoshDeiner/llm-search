class SearchTermService:
    def create_search_term(self, user_input: str) -> str:
        """Generates a search term based on user input."""
        return user_input.strip()