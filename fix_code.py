from CodeGeneration.Completions import get_gpt4_completion
from utils import code_extractor
from prompts import Prompts

class FixCode:
    """
    Handles operations related to correcting code using GPT-4 based on error messages.
    """
    
    @staticmethod
    def fix_code(python_code: str, error_message: str) -> dict:
        fix_prompt = Prompts.fix_code(python_code, error_message)
        try:
            corrected_code = code_extractor(get_gpt4_completion(fix_prompt))
            return {
                "corrected_code": corrected_code
            }
        except Exception as e:
            return {
                "error": f"Error in code correction: {str(e)}"
            }
