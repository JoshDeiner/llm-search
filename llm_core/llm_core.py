# llm_core/llm_core.py

class LLMCore:
    def generate_text(self, prompt: str) -> str:
        """Generates text based on a given prompt."""
        raise NotImplementedError("This method should be implemented by a specific LLM.")

    def summarize_text(self, text: str) -> str:
        """Summarizes the given text."""
        # By default, you can define summarization as calling generate_text with a summarization prompt.
        summary_prompt = f"Summarize the following:\n\n{text}"
        return self.generate_text(summary_prompt)
