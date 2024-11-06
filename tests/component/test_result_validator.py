from src.core_pipeline.validators.result_validator import validate_search_engine_results

def test_validate_search_engine_results():
    search_data = {
        "web_results": [{"title": "Valid Result"}, {"title": "Invalid Result"}],
        "validation_results": [{"is_valid": True}, {"is_valid": False}],
    }
    validated_results = validate_search_engine_results(search_data)

    # Check that only one result is returned
    assert len(validated_results) == 1, "Expected only one validated result"
    
    # Check that the returned result is the valid one
    assert validated_results[0]["title"] == "Valid Result", "Expected title to be 'Valid Result'"
