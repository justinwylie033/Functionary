import os
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt
import openai

def _ensure_api_key(func):
    """Decorator to ensure that the OpenAI API key is set."""
    
    def wrapper(*args, **kwargs):
        # Load environment variables using python-dotenv
        load_dotenv()
        # Get OpenAI key using os.environ
        OPEN_AI_KEY = os.environ.get('OPEN_AI_KEY')

        if not openai.api_key:
            openai.api_key = OPEN_AI_KEY
        return func(*args, **kwargs)
    return wrapper

@_ensure_api_key
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def _make_openai_call(model, prompt, temperature):
    try:
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": f"generate {prompt}"}
            ],
            temperature=temperature
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error fetching {model} completion: {str(e)}"


@_ensure_api_key
def get_gpt_completion(prompt):
    """Use GPT-3.5-turbo to generate the content based on the prompt."""
    return _make_openai_call("gpt-3.5-turbo", prompt, 0.55)

@_ensure_api_key
def get_gpt4_completion(prompt):
    """Use GPT-4 to generate the content based on the prompt."""
    return _make_openai_call("gpt-4", prompt, 1.0)

@_ensure_api_key
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(text, model="text-embedding-ada-002"):
    try:
        response = openai.Embedding.create(input=text, model=model)
        return response['data'][0]['embedding']
    except Exception as e:
        return f"Error getting embedding for text using {model}: {str(e)}"

