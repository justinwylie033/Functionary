from typing import Optional
from Functionary.PromptEngineering.prompts import Prompts
from Functionary.Utils.utils import Utils
from Functionary.Generation.Completions import get_gpt4_completion




class CodeGeneration:
    """
    Handles operations related to generating code using GPT-4.
    """
    
    @staticmethod
    def generate_function_prompt(user_prompt: str) -> str:
        """
        Generates a function prompt based on the user's input.

        Args:
        - user_prompt (str): The user's input for generating the prompt.

        Returns:
        - str: The generated function prompt.
        """
        return Prompts.function(user_prompt)

    @staticmethod
    def generate_code_from_user_prompt(user_prompt: str) -> Optional[str]:
        """
        Generates code using GPT-4 based on the user's input.

        Args:
        - user_prompt (str): The user's input for generating the code.

        Returns:
        - Optional[str]: The generated code if successful, otherwise None.
        """
        prompt = CodeGeneration.generate_function_prompt(user_prompt)
        try:
            return Utils.code_extractor(get_gpt4_completion(prompt))
        except Exception:
            # Log the error or issue, but do not disrupt the flow.
            return None
