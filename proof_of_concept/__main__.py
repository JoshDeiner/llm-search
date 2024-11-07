from langchain_community.utilities import SearxSearchWrapper
from typing import List
from typing import Dict

from src.constants import WEB_SEARCH_URL


"""

* should you make run and results async? 
* how to do so?

https://python.langchain.com/api_reference/community/utilities/langchain_community.utilities.searx_search.SearxSearchWrapper.html#langchain_community.utilities.searx_search.SearxSearchWrapper.results
"""


def search_with_searx(
    query: str, 
    num_results: int, 
    engines: List[str] = None,
    categories: List[str] = None,
    query_suffix: str = '',
    **kwargs) -> List[Dict]:
    """Perform a search using Searx and return results."""
    
    # Initialize the Searx search wrapper
    search_wrapper = SearxSearchWrapper(searx_host=WEB_SEARCH_URL)
    
    # Call the results method
    results = search_wrapper.results(
        query=query,
        num_results=num_results,
        engines=engines,
        categories=categories,
        query_suffix=query_suffix,
        **kwargs
    )
    
    return results

# Example usage
if __name__ == '__main__':
    query = "what happened to the new york giants in the last quarter 2024"
    num_results = 10  # Specify the number of results you want
    custom_engines =  ["bing", "google"]
    default_engines = None
    engines = custom_engines   # You can specify a list of engines or leave it as None
    cc = ["politics"]
    default_categories = None
    categories = default_categories # You can specify a list of categories or leave it as None

    results = search_with_searx(query, num_results, engines, categories)
    
    # Print the results
    for result in results:
        print(f'\n Title: {result.get("title")}, \n URL: {result.get("link")}, \n Snippet: {result.get("snippet")}')
