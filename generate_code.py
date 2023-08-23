from CodeGeneration.Completions import get_gpt4_completion
from Docker.DockerFunctions import DockerFunctions
from utils import code_extractor
from DB.db import FunctionaryDB
from prompts import Prompts

class CodeGeneration:
    """
    Handles operations related to generating code using GPT-4.
    """
    
    @staticmethod
    def generate_function_prompt(user_prompt: str) -> str:
        return Prompts.function(user_prompt)
    
    @staticmethod
    def generate_big_o_prompt(code: str) -> str:
        return Prompts.big_o(code)

    @staticmethod
    def generate_code(prompt: str) -> str:
        try:
            return code_extractor(get_gpt4_completion(prompt))
        except Exception as e:
            raise RuntimeError(f"Error in code generation: {str(e)}")
    
    @staticmethod
    def get_big_o_notation(code: str) -> str:
        big_o_prompt = CodeGeneration.generate_big_o_prompt(code)
        try:
            return get_gpt4_completion(big_o_prompt)
        except Exception as e:
            raise RuntimeError(f"Error in retrieving Big O notation: {str(e)}")
