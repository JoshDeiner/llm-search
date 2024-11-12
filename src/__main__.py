import logging
import argparse
import os
from dotenv import load_dotenv

from src.core_pipeline.execute_pipeline import execute_pipeline
from src.features.users.factory import create_user_service

# Configure logging with timestamp
logging.basicConfig(
    filename="./logs/query.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

SEARCH_TERM_GLOBAL: str = "who do the giants play november 10 in germany"


def cli_entry() -> None:
    """
    CLI entry point for the search and summary pipeline.
    Parses the search term argument, initializes environment, and runs the main pipeline.
    """
    # Load environment variables and check if loaded successfully
    if not load_dotenv():
        logging.warning(
            "Could not load environment variables. Ensure .env file exists."
        )

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Search with search_engine")
    parser.add_argument(
        "search_term",
        nargs="?",
        default=SEARCH_TERM_GLOBAL,
        help="The search term to query the search engine",
    )
    args: argparse.Namespace = parser.parse_args()

    # Run the main pipeline with parsed search term
    logging.info("Starting search and summarization process")
    execute_pipeline(create_user_service(), args.search_term)
    logging.info("Search and summarization process completed.")


if __name__ == "__main__":
    cli_entry()
