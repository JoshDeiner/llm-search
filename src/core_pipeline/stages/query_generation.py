# doesn't look used


def generate_query(search_term: str) -> dict[str, str]:
    """
    Generates a structured query based on the user-provided search term.

    Parameters:
    search_term (str): The user’s input for what they want to search.

    Returns:
    dict: A dictionary representing the formatted query for the search engine.
    """
    # For example, you might want to add parameters or preprocess the term
    formatted_query = {"query": search_term.strip().lower()}
    return formatted_query
