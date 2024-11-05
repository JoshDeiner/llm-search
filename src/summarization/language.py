import subprocess


# probably get rid of once summary is up
class OllamaConfig:
    _instance = None  # Singleton instance

    def __init__(self, model_name="llama3.2:latest"):
        """Private initializer to prevent direct instantiation."""
        if OllamaConfig._instance is None:
            self._model_name = model_name  # Private attribute for model name
            OllamaConfig._instance = self

    @classmethod
    def get_instance(cls):
        """Method to get the singleton instance of OllamaConfig."""
        if cls._instance is None:
            cls()  # Instantiate if it hasn't been created yet
        return cls._instance

    # fix later TODO!!!
    def generate_response(self, prompt):
        """Method to generate a response from the local Ollama model."""
        process = subprocess.Popen(
            ["ollama", "run", self._model_name],
            text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate(input=prompt)

        if process.returncode != 0:
            raise RuntimeError(f"Error running model: {stderr}")

        return stdout.strip()  # Return the generated response

    @property
    def model_name(self):
        """Getter for the model name if access is needed."""
        return self._model_name


# Usage example
if __name__ == "__main__":
    ollama_llm = OllamaConfig.get_instance()
    response = ollama_llm.generate_response("Explain how machine learning works")
    print(response)
