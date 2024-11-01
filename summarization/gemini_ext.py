import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


class GeminiLLM:
    _instance = None

    def __init__(self, model_name="gemini-1.5-flash"):
        """Initialize the Gemini model with configuration from environment variables."""
        if GeminiLLM._instance is None:
            GEMINI_KEY = os.getenv("GEMINI_KEY")
            self._model_name = model_name
            genai.configure(api_key=GEMINI_KEY)
            self.model = genai.GenerativeModel(self._model_name)
            GeminiLLM._instance = self
        else:
            raise Exception(
                "GeminiLLM instance already exists. Use get_instance() instead."
            )

    @classmethod
    def get_instance(cls):
        """Singleton access method for the GeminiLLM class."""
        if cls._instance is None:
            cls._instance = GeminiLLM()
        return cls._instance

    def generate_response(self, prompt):
        """Generates a response from the Gemini model for a given prompt."""
        response = self.model.generate_content(prompt)
        return response.text

    @property
    def model_name(self):
        """Getter for the model name if access is needed."""
        return self._model_name


# Usage example
if __name__ == "__main__":
    gemini_llm = GeminiLLM.get_instance()
    response = gemini_llm.generate_response("Explain how AI works")
    print(response)
