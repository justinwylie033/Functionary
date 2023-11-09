from typing import Optional, Dict, Union
from Generation.Complete import Completions
from Utils.utils import Utils
from PromptEngineering.prompts import Prompts

class FixCode:

    def __init__(self):
        self.completions = Completions()
        
    """
    Handles operations related to correcting code using GPT-4 based on error messages.
    """
    
    @staticmethod
    def fix_code(self, python_code: str, error_message: str) -> Dict[str, Union[str, None]]:
        """
        Attempts to correct the provided code using GPT-4 based on an error message.

        Args:
        - python_code (str): The original code that needs fixing.
        - error_message (str): The error message associated with the original code.

        Returns:
        - Dict[str, Union[str, None]]: A dictionary containing the corrected code or an error message.
        """
        fix_prompt = Prompts.fix_code(python_code, error_message)
        
        try:
            corrected_code = Utils.code_extractor(self.completions.get_gpt4_completion(fix_prompt))
            return {
                "corrected_code": corrected_code
            }
        except Exception:
            # Log the error or issue, but do not disrupt the flow.
            # Return a dictionary indicating that the code correction was unsuccessful.
            return {
                "corrected_code": None
            }
