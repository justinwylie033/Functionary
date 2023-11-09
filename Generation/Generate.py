from typing import Optional
import logging
from dotenv import load_dotenv
from PromptEngineering.prompts import Prompts
from Utils.utils import Utils
from Generation.Complete import Completions  # Ensure this path is correct

logging.basicConfig(level=logging.INFO)

class Generate:
    """
    Handles operations related to generating code using GPT-4.
    """

    def __init__(self):
        # Load the environment variables and instantiate the Completions class
        load_dotenv()
        self.completions = Completions()

    def generate_execution_commmand(self, code):
        return self.completions.get_gpt4_completion(Prompts.execution_command(code))

    def generate_description_from_code(self, code: str) -> Optional[str]:
        """
        Generates a description using GPT-4 based on the given Python function code.
        """
        prompt = Prompts.describe_code(code)
        try:
            # Assuming that get_gpt4_completion directly returns the generated text.
            return self.completions.get_gpt4_completion(prompt)
        except Exception as e:
            logging.error(f"Failed to generate description: {str(e)}")
            return None

    def generate_function(self, user_prompt: str) -> Optional[str]:
        """
        Generates function using GPT-4 based on the user's input.
        """
        prompt = Prompts.function(user_prompt)
        try:
            completion = self.completions.get_gpt4_completion(prompt)
            return Utils.code_extractor(completion)
        except Exception as e:
            logging.error(f"Failed to generate function: {str(e)}")
            return None
        
    def generate_class(user_prompt: str) -> Optional[str]:
        """Generates a class"""

    def generate_program(user_prompt: str) -> Optional[str]:
        """Generates a full program"""

if __name__ == '__main__':
    # Example usage:
    generation = Generate()
    print(generation.generate_function("tic tac toe"))


