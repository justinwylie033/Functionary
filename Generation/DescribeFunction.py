# DescribeFunction.py

from typing import Optional
from Functionary.PromptEngineering.prompts import Prompts  # Assuming Prompts is part of this module
from Functionary.Utils.utils import Utils
from Functionary.Generation.Completions import get_gpt4_completion

class DescribeFunction:
    """
    Handles operations related to describing a given Python function using GPT-4.
    """

    @staticmethod
    def generate_description_prompt(function_code: str) -> str:
        """
        Generates a description prompt based on the given Python function.

        Args:
        - function_code (str): The code of the Python function to describe.

        Returns:
        - str: The generated description prompt.
        """
        return Prompts.describe_function(function_code)

    @staticmethod
    def generate_description_from_code(function_code: str) -> Optional[str]:
        """
        Generates a description using GPT-4 based on the given Python function code.

        Args:
        - function_code (str): The code of the Python function to describe.

        Returns:
        - Optional[str]: The generated description if successful, otherwise None.
        """
        prompt = DescribeFunction.generate_description_prompt(function_code)
        try:
            # Assuming that get_gpt4_completion directly returns the generated text.
            return get_gpt4_completion(prompt)
        except Exception:
            # Log the error or issue, but do not disrupt the flow.
            return None
