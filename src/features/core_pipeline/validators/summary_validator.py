import logging
import pprint

from src.features.llm_core.llm_core import LLMCore


def validate_summary(llm_core: LLMCore, results_text: str) -> bool:
    summary = llm_core.summarize_text(results_text)
    logging.info("Generated Summary:")
    logging.info(summary)

    try:
        summary_validation_result = llm_core.validate_and_score_summary(
            summary, results_text
        )
    except Exception as e:
        logging.error(f"Error during summary validation: {e}")
        return False

    logging.info("Summary Validation Result:")
    logging.info(pprint.pformat(summary_validation_result))

    if summary_validation_result.get("is_valid", False):
        logging.info("Summary validation succeeded.")
        logging.info("Final Summary:")
        logging.info(summary)
        return True
    else:
        logging.warning(
            f"Summary validation failed: {summary_validation_result.get('reason', 'Unknown reason')}"
        )
        return False
