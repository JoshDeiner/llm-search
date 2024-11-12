import ollama
from typing import Optional
from typing import Generator
from typing import Any


class OllamaLLM:
    def __init__(self, model_name: str = "llama3.2:latest") -> None:
        """
        Initialize the Ollama model with the specified model name.
        """
        self._model_name: str = model_name  # Private attribute for model name
        self.client: ollama = ollama  # Set up client as an instance attribute

    def generate_response(self, prompt: str) -> Optional[str]:
        """
        Method to generate a response from the Ollama model.

        Args:
            prompt (str): The input prompt for the model.

        Returns:
            Optional[str]: The generated response or None if unavailable.
        """
        return self.client.generate(model=self._model_name, prompt=prompt)

    def generate_streaming_response(self, prompt: str) -> Generator[str, None, None]:
        """
        Generator function to stream the model output.

        Args:
            prompt (str): The input prompt for the model.

        Yields:
            str: Streaming output from the model.
        """
        for output in self.client.generate(
            model=self._model_name, prompt=prompt, stream=True
        ):
            yield output
