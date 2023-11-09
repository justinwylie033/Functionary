from typing import Optional
PromptEngineering.prompts import Prompts
Generation.Completions import get_gpt4_completion

class CodeAnalyser:
    """
    A utility class for code analysis and related operations.
    """

    @staticmethod
    def generate_big_o_prompt(code: str) -> str:
        """
        Generates a prompt for Big O notation based on the provided code.

        Args:
        - code (str): The code to generate a prompt for.

        Returns:
        - str: The generated prompt.
        """
        # Assuming that Prompts is another module or class that you have,
        # the actual implementation might differ based on where it's located.
        return Prompts.big_o(code)

    @staticmethod
    def get_big_o_notation(code: str) -> Optional[str]:
        """
        Determines the Big O notation for the given code.

        Args:
        - code (str): The code for which to get the Big O notation.

        Returns:
        - str: The Big O notation for the provided code if successful, otherwise None.
        """
        big_o_prompt = CodeAnalyser.generate_big_o_prompt(code)
        
        # Assuming that get_gpt4_completion is another function or method you have,
        # the actual implementation might differ based on where it's located.
        notation = get_gpt4_completion(big_o_prompt)
        
        if not notation:
            # Log the error or issue, but do not disrupt the flow.
            return None
        return notation
