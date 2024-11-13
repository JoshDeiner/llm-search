import pytest
from src.features.core_pipeline.validators.result_validator import (
    validate_search_engine_results,
)


def test_validate_search_engine_results():
    search_data = {
        "web_results": [{"title": "Valid Result"}, {"title": "Invalid Result"}],
        "validation_results": [{"is_valid": True}, {"is_valid": False}],
    }
    validated_results = validate_search_engine_results(search_data)

    # Check that only one result is returned
    assert len(validated_results) == 1, "Expected only one validated result"

    # Check that the returned result is the valid one
    assert (
        validated_results[0]["title"] == "Valid Result"
    ), "Expected title to be 'Valid Result'"


def test_validate_search_engine_results_no_validations():
    """
    Test validate_search_engine_results returns all results when no validation data is provided.
    """
    search_data = {
        "web_results": [{"title": "Result 1"}, {"title": "Result 2"}],
        "validation_results": [],
    }
    validated_results = validate_search_engine_results(search_data)

    # Check that all results are returned when no validation data is provided
    assert len(validated_results) == 2, "Expected all results to be returned"
    assert validated_results[0]["title"] == "Result 1"
    assert validated_results[1]["title"] == "Result 2"


def test_validate_search_engine_results_invalid_input():
    search_data = {
        "web_results": "Invalid Data",
        "validation_results": "Invalid Data",
    }
    validated_results = validate_search_engine_results(search_data)

    # Check that the function handles invalid input gracefully
    assert validated_results == [], "Expected an empty list for invalid input"


def test_validate_search_engine_results_mismatched_lengths():
    search_data = {
        "web_results": [{"title": "Result 1"}],
        "validation_results": [{"is_valid": True}, {"is_valid": False}],
    }
    validated_results = validate_search_engine_results(search_data)

    # Check that the function handles mismatched lengths gracefully
    assert (
        validated_results == []
    ), "Expected an empty list for mismatched input lengths"
