import pytest
from src.features.users.services.user_query_validation_service import QueryValidationService
from src.features.llm_core.llm_provider import LLMProvider

@pytest.fixture
def llm_provider():
    return LLMProvider(model_name="gemini")

@pytest.fixture
def query_validation_service(llm_provider):
    return QueryValidationService(llm_provider)

def test_has_category_relationship(query_validation_service):
    query = "who do the new york giants play on november 17th 2024"
    result = query_validation_service.has_category_relationship(query)
    print("res", result)
    assert result == 1.0, "Expected the query to have a relationship to predefined categories."

    # query = "random unrelated query"
    # result = query_validation_service.has_category_relationship(query)
    # assert result == 0.0, "Expected the query to not have a relationship to predefined categories."

# def test_query_validator(query_validation_service):
#     query = "latest sports news"
#     score = query_validation_service.query_validator(query)
#     assert score > 0, "Expected a positive score for a valid query."

#     query = "random unrelated query"
#     score = query_validation_service.query_validator(query)
#     assert score == 0, "Expected a score of 0 for an unrelated query."

# def test_executor(query_validation_service):
#     query = "latest sports news"
#     result = query_validation_service.executor(query)
#     assert result["isValid"], "Expected the query to be valid."
#     assert result["response"] == "successful response", "Expected a successful response."

#     query = "random unrelated query"
#     result = query_validation_service.executor(query)
#     assert not result["isValid"], "Expected the query to be invalid."
#     assert result["response"] == "Query does not have relationship to categories", "Expected a specific error message."