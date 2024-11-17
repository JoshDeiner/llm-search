import sys
import os


# Add the root directory of the project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from src.features.llm_core.llm_provider import LLMProvider

class QueryValidationService:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    categories = [
        "historical lookup", "urgent news", "weekly updates", 
        "sporting events", "political events", "world events", "climate change"
    ]

    def query_validator(self, query: str) -> float:
        # Perform semantic analysis or use LLM to categorize the query
        category_score = self.has_category_relationship(query)
        if not category_score:
            return 0.0
        
        # Check if the query is ingestible for a search engine
        ingestible_score = self.is_ingestible_for_search_engine(query)
        if not ingestible_score:
            return 0.0
        
        # Check if the query aligns with the project's goals
        goal_alignment_score = self.aligns_with_project_goals(query)
        if not goal_alignment_score:
            return 0.0
        
        # Calculate the final score (example logic, can be adjusted)
        final_score = (category_score + ingestible_score + goal_alignment_score) / 3
        return final_score

    def executor(self, query: str) -> dict:
        try:
            score = self.query_validator(query)
            if score == 0:
                return {"isValid": False, "response": "Query does not have relationship to categories"}
            elif score < 0.5:
                return {"isValid": False, "response": "Query is of low quality"}
            else:
                return {"isValid": True, "response": "successful response"}
        except Exception as e:
            return {"isValid": False, "response": str(e)}

    def has_category_relationship(self, query: str) -> float:
        print("query", query)
        pass
        # this probably is not a score but is a boolean expression
        # is there a categorical relationship
        # is there a semantical simarility between the text meaning and the category
        # if so return true or one
        # else return false or zero

    

    def is_ingestible_for_search_engine(self, query: str) -> float:
        # Example logic to determine if the query is ingestible for a search engine
        if len(query) > 5 and not any(char in query for char in "@#$%^&*()"):
            return 1.0
        return 0.0

    def aligns_with_project_goals(self, query: str) -> float:
        # Example logic to determine if the query aligns with the project's goals
        goals = ["sports", "politics", "entertainment"]
        for goal in goals:
            if goal in query.lower():
                return 1.0
        return 0.0

if __name__ == "__main__":
    # Example usage
    llm_provider = LLMProvider(model_name="gemini")
    query_validation_service = QueryValidationService(llm_provider)

    query = "who do the new york giants play on november 17th 2024"
    res = query_validation_service.has_category_relationship(query)
    print("res", res)
    # queries = [
    #     "latest sports news",
    #     "random unrelated query",
    #     "what year did Bell Labs begin its program",
    #     "@#$%^&*()",
    #     ""
    # ]

    # for query in queries:
    #     result = query_validation_service.executor(query)
    #     print(f"Query: {query}\nResult: {result}\n")




