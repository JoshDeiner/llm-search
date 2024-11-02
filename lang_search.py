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
    load_dotenv()

    user_service = get_user_service()

    # Run search process to get raw results
    web_results = user_service.search(search_term)
    logging.info(f"Raw web search results: {web_results}")

    # Combine the search results for summarization
    results_text = "\n\n".join(
        web_results
    )  # Concatenates all results with double line breaks

    # Initialize the LLM provider
    llm_core = LLMProvider(model_name="gemini")

    # Generate and validate the summary
    summary = llm_core.summarize_text(results_text)
    validation_result = llm_core.validate_and_score_summary(summary, results_text)

    # Log and output results based on validation
    if validation_result["is_valid"]:
        logging.info("Summary is valid according to validation criteria.")
        print("Final Summary:", summary)
        print("Validation Result:", validation_result)
    else:
        logging.warning(f"Summary validation failed: {validation_result['reason']}")
        logging.info(
            f"Summary did not meet criteria after retries. Final score: {validation_result['score']}"
        )
        print("Final Summary (Unvalidated):", summary)
        print("Final Validation Result:", validation_result)


if __name__ == "__main__":

    # Parse CLI argument for the search term
    parser = argparse.ArgumentParser(description="Search with search_engine")
    parser.add_argument(
        "search_term",
        nargs="?",
        default="what do the experts say about the yankees struggles vs the dodgers",
        help="The search term to query search_engine",
    )

    args = parser.parse_args()

    # Execute main function with the provided search term
    main(args.search_term)
    logging.info("Search process completed.")
