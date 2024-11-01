import pprint
import logging
import argparse
import os

from dotenv import load_dotenv

from langchain_community.utilities import SearxSearchWrapper

from user_service.factory import get_user_service
from services.search_service import init_searxng_host

logging.basicConfig(filename="./logs/query.log", level=logging.INFO)

# Instantiate User with injected dependencies
# probably to switch based on if docker or not
# Instantiate User with dependencies


# def get_search_results(query: str):
#     logging.info(f"Executing search query: {query}")
#     search = init_searxng_host()
#     r = search.run(query, language="en-us")
#     logging.info(f"Search results: {r}")
#     return r


# def main(search_term: str):
#     load_dotenv()
#     logging.info("Starting main execution")
#     logging.info(f"Search term in main: {search_term}")
#     results = get_search_results(search_term)
#     pprint.pprint(results)
#     logging.info("Finished main execution")


if __name__ == "__main__":
    load_dotenv()

    logging.info("init main")

    parser = argparse.ArgumentParser(description="Search with search_engine")
    parser.add_argument(
        "search_term",
        nargs="?",
        default="ai news october",
        help="The search term to query search_engine",
    )

    args = parser.parse_args()

    # Pass the argument to main
    # main(args.search_term)

    user_service = get_user_service()

    # Run search process to get raw results
    web_results = user_service.search(args.search_term)
    print("Web Search Results:", web_results)
