import pprint
import logging
import argparse
import os

from dotenv import load_dotenv
from llm_core.llm_provider import LLMProvider  # Import LLM provider
from user_service.factory import get_user_service
from requests.exceptions import RequestException  # Example of handling network errors

logging.basicConfig(filename="./logs/query.log", level=logging.INFO)


def validate_se_results(search_data):
    """
    Validate search engine (SE) results based on the search query.

    Parameters:
    search_data (dict): Dictionary containing search results and validation information.

    Returns:
    list: A list of validated search engine results, or all results as a fallback if none are validated.
    """
    web_results = search_data.get("web_results", [])
    se_validation_results = search_data.get("validation_results", [])

    # Log raw web results and validation results for debugging
    logging.info("Raw web search results:")
    logging.info(pprint.pformat(web_results))
    logging.info("Search engine validation results:")
    logging.info(pprint.pformat(se_validation_results))

    # Filter search engine validated results
    validated_se_results = [
        result
        for result, validation in zip(web_results, se_validation_results)
        if validation.get("is_valid", False)
    ]

    # If no results are validated by the search engine, use all results as fallback
    return validated_se_results if validated_se_results else web_results


def validate_summary(llm_core, results_text):
    """
    Generates a summary from results text and validates it using LLMCore’s built-in retry mechanism.

    Parameters:
    - llm_core (LLMCore): The LLM provider instance.
    - results_text (str): The text to summarize and validate.

    Returns:
    bool: True if validation succeeds, False otherwise.
    """
    # Generate the summary
    summary = llm_core.summarize_text(results_text)
    logging.info("Generated Summary:")
    logging.info(summary)

    # Validate the summary
    try:
        summary_validation_result = llm_core.validate_and_score_summary(summary, results_text)
    except Exception as e:
        logging.error(f"Error during summary validation: {e}")
        return False

    # Log validation results for the summary
    logging.info("Summary Validation Result:")
    logging.info(pprint.pformat(summary_validation_result))

    if summary_validation_result.get("is_valid"):
        logging.info("Summary validation succeeded.")
        logging.info("Final Summary:")
        logging.info(summary)
        return True
    else:
        logging.warning(f"Summary validation failed: {summary_validation_result.get('reason')}")
        return False


def search_and_validate(user_service, search_term):
    """
    Perform a search and validate the results.
    """
    try:
        search_data = user_service.search(search_term)
        return validate_se_results(search_data)
    except RequestException as e:
        logging.error(f"Network error: {e}")
        return None


def retry_with_validation(func, *args, max_retries=3):
    """
    Retry a function that requires validation, with a maximum number of retries.
    """
    for attempt in range(1, max_retries + 1):
        logging.info(f"Attempt {attempt} of {max_retries}")
        
        results = func(*args)
        if results:
            logging.info("Validation succeeded.")
            return results
        else:
            logging.warning("Validation failed or network error. Retrying...")
            if attempt == max_retries:
                logging.error("All retries exhausted. Validation failed.")
                return None


def main(search_term: str):
    logging.info("Initializing search process")
    load_dotenv()

    user_service = get_user_service()
    llm_core = LLMProvider(model_name="gemini")

    # Use retry_with_validation to perform search with validation
    validated_se_results = retry_with_validation(search_and_validate, user_service, search_term)

    if validated_se_results is None:
        logging.error("Search and validation process failed.")
        return

    # Combine validated search engine results for summarization
    results_text = "\n\n".join(validated_se_results)

    # Generate the summary and validate it
    if not validate_summary(llm_core, results_text):
        logging.error("Summary generation and validation failed.")
        return
    logging.info("Summary generation and validation succeeded.")


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
