import os
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt
import openai

class Completions:

    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get('OPEN_AI_KEY')

        if not self.api_key:
            raise ValueError("No OpenAI API key found. Please set the OPEN_AI_KEY environment variable.")

        openai.api_key = self.api_key

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def _make_openai_call(self, model, prompt, temperature):
        try:
            completion = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": f"generate {prompt}"}],
                temperature=temperature
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error fetching {model} completion: {str(e)}")

    def get_gpt_completion(self, prompt):
        """Use GPT-3.5-turbo to generate the content based on the prompt."""
        return self._make_openai_call("gpt-3.5-turbo", prompt, 0.55)

    def get_gpt4_completion(self, prompt):
        """Use GPT-4 to generate the content based on the prompt."""
        return self._make_openai_call("gpt-4", prompt, 1.0)

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def get_embedding(self, text, model="text-embedding-ada-002"):
        try:
            response = openai.Embedding.create(input=text, model=model)
            return response['data'][0]['embedding']
        except Exception as e:
            raise Exception(f"Error getting embedding for text using {model}: {str(e)}")
        
if __name__ == "__main__":
    completion = Completions()


