import pprint
import logging
import argparse
from dotenv import load_dotenv

import os

from langchain_community.utilities import SearxSearchWrapper

logging.basicConfig(filename='./logs/query.log', level=logging.INFO)
# Configure logging
logging.basicConfig(level=logging.INFO)

def init_searxng_host():

    is_docker = os.getenv("IS_DOCKER") == "true"
    host = "http://searxng-instance:8080/search" if is_docker else "http://localhost:8888/search"

    output = 3
    search = SearxSearchWrapper(searx_host=host, k=output)
    logging.info("SearxNG host initialized")
    return search

def get_search_results(query: str):
    logging.info(f"Executing search query: {query}")
    search = init_searxng_host()
    r = search.run(query, language="en-us")
    logging.info(f"Search results: {r}")
    return r

def main(search_term: str):
    load_dotenv()
    logging.info("Starting main execution")
    logging.info(f"Search term in main: {search_term}")
    results = get_search_results(search_term)
    pprint.pprint(results)
    logging.info("Finished main execution")


if __name__ == "__main__":
    logging.info("init main")
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Search with SearxNG")
    parser.add_argument(
        "search_term",
        nargs="?",
        default="who do the yankees play next",
        help="The search term to query SearxNG with"
    )

    args = parser.parse_args()
    
    # Pass the argument to main
    main(args.search_term)