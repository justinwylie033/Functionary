from tenacity import retry, wait_random_exponential, stop_after_attempt, RetryError
import openai
from decouple import config

# Initialise OpenAI key
OPEN_AI_KEY = config('OPEN_AI_KEY')
openai.api_key = OPEN_AI_KEY

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def _make_openai_call(model, prompt, temperature):
    """Internal helper function to make API calls to OpenAI."""
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": f"generate {prompt}"}
        ],
        temperature=temperature
    )
    return completion.choices[0].message.content

def get_gpt_completion(prompt):
    """Use GPT-3.5-turbo to generate the content based on the prompt."""
    try:
        return _make_openai_call("gpt-3.5-turbo", prompt, 0.55)
    except (RetryError, Exception) as e:
        raise Exception(f"Error fetching GPT-3.5-turbo completion: {str(e)}")

def get_gpt4_completion(prompt):
    """Use GPT-4 to generate the content based on the prompt."""
    try:
        return _make_openai_call("gpt-4", prompt, 1.0)
    except (RetryError, Exception) as e:
        raise Exception(f"Error fetching GPT-4 completion: {str(e)}")

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(text, model="text-embedding-ada-002"):
    response = openai.Embedding.create(input=text, model=model)
    embedding = response['data'][0]['embedding']
    return embedding

