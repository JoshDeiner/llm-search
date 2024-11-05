# import logging
# import argparse
# import os
# from dotenv import load_dotenv

# from llm_core.llm_provider import LLMProvider
# from user_service.factory import get_user_service
# from core_pipeline.stages.search_execution import search_and_validate, retry_with_validation
# from core_pipeline.stages.data_processing import process_results
# from core_pipeline.stages.summarization import summarize_results
# from core_pipeline.validators.summary_validator import validate_summary

# from services.search_engine_client import SearchEngineClient

# logging.basicConfig(filename="./logs/query.log", level=logging.INFO)

# SEARCH_TERM_GLOBAL = "where to find the best muffin in north america"

# def main(search_term: str):
#     logging.info("Initializing search process")
#     load_dotenv()

#     # Initialize services
#     user_service = get_user_service()
#     llm_core = LLMProvider(model_name="gemini")

#     # Step 1: Search and validate results
#     validated_se_results = retry_with_validation(search_and_validate, user_service, search_term)

#     if validated_se_results is None:
#         logging.error("Search and validation process failed.")
#         return

#     # Step 2: Process results for summarization
#     results_text = process_results(validated_se_results)

#     # Step 3: Summarize the results
#     summary = summarize_results(llm_core, results_text)
#     if summary is None:
#         logging.error("Summary generation failed.")
#         return

#     # Step 4: Validate the summary
#     if not validate_summary(llm_core, results_text):
#         logging.error("Summary generation and validation failed.")
#         return

#     logging.info("Summary generation and validation succeeded.")
#     logging.info("Final Summary:")
#     logging.info(summary)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Search with search_engine")
#     parser.add_argument("search_term", nargs="?", default=SEARCH_TERM_GLOBAL, help="The search term to query search_engine")

#     args = parser.parse_args()
#     main(args.search_term)
#     logging.info("Search process completed.")


import logging
import argparse
import os
from dotenv import load_dotenv

from core_pipeline.main_pipeline import main_pipeline
from user_service.factory import get_user_service

logging.basicConfig(filename="./logs/query.log", level=logging.INFO)

SEARCH_TERM_GLOBAL = "where to find the best muffin in North America"


def cli_entry():
    """
    CLI entry point for the search and summary pipeline.
    Parses the search term argument, initializes environment, and runs the main pipeline.
    """
    # Load environment variables
    load_dotenv()

    # Initialize user service
    user_service = get_user_service()

    dude = user_service.search("where am i")
    print("dude", dude)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Search with search_engine")
    parser.add_argument(
        "search_term",
        nargs="?",
        default=SEARCH_TERM_GLOBAL,
        help="The search term to query the search engine",
    )
    args = parser.parse_args()

    # Run the main pipeline with parsed search term
    logging.info("Starting search and summarization process")
    main_pipeline(user_service, args.search_term)
    logging.info("Search and summarization process completed.")


if __name__ == "__main__":
    cli_entry()
