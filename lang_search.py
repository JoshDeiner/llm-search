import pprint
import logging
import argparse
import os

from dotenv import load_dotenv
from llm_core.llm_provider import LLMProvider  # Import LLM provider
from user_service.factory import get_user_service
from services.search_service import init_searxng_host

logging.basicConfig(filename="./logs/query.log", level=logging.INFO)

def main(search_term: str):
    logging.info("Initializing search process")
    user_service = get_user_service()
    
    # Run search process to get raw results
    web_results = user_service.search(search_term)
    logging.info(f"Raw web search results: {web_results}")

    # Summarize the combined text with LLM
    llm_core = LLMProvider(model_name="gemini")
    results_text = web_results

    summary = llm_core.summarize_text(results_text)

    # logging.info(f"Summary of web search results: {summary}")
    
    # Output results
    logging.info("Search Results:")

    logging.info(web_results)
    logging.info("")
    logging.info("")

    logging.info("Web Search Results Summary:")
    logging.info(summary)
    pprint.pprint(summary)

if __name__ == "__main__":
    load_dotenv()
    
    # Parse CLI argument for the search term
    parser = argparse.ArgumentParser(description="Search with search_engine")
    parser.add_argument(
        "search_term",
        nargs="?",
        default="wake me up when september ends",
        help="The search term to query search_engine",
    )
    args = parser.parse_args()

    # Execute main function with the provided search term
    main(args.search_term)
    logging.info("Search process completed.")
