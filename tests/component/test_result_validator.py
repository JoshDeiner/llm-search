from core_pipeline.validators.result_validator import validate_se_results


def test_validate_se_results():
    search_data = {
        "web_results": [{"title": "Valid Result"}, {"title": "Invalid Result"}],
        "validation_results": [{"is_valid": True}, {"is_valid": False}],
    }
    validated_results = validate_se_results(search_data)

    assert len(validated_results) == 1  # Only the valid result should be returned
    assert validated_results[0]["title"] == "Valid Result"
