import unittest
from Functionary.Generation.Completions import get_gpt_completion, get_gpt4_completion, get_embedding

class TestOpenAIApiCallsWithRealAPI(unittest.TestCase):

    # For GPT completions (both 3.5 and 4):
    def test_get_gpt_completion_happy_path(self):
        prompt = "Hello"
        response = get_gpt_completion(prompt)
        self.assertIsInstance(response, str)

    def test_get_gpt4_completion_happy_path(self):
        prompt = "Hello"
        response = get_gpt4_completion(prompt)
        self.assertIsInstance(response, str)

    # For embedding:
    def test_get_embedding_happy_path(self):
        text = "Hello"
        response = get_embedding(text)
        self.assertIsInstance(response, (str, list))

    # Test invalid models
    def test_invalid_model_for_gpt(self):
        response = get_gpt_completion("Hello", model="invalid-model")
        self.assertIn("Error", response)

    def test_invalid_model_for_embedding(self):
        response = get_embedding("Hello", model="invalid-model")
        self.assertIn("Error", response)

    # Test rate limits and retry error
    def test_retry_error(self):
        # Just testing that the error handling works. Rate limits are hard to test programmatically.
        response = get_gpt_completion("test retry")
        self.assertIn(response, ["success", "error"])

    # Test empty prompt
    def test_empty_prompt_gpt_completion(self):
        response = get_gpt_completion("")
        self.assertIn("success", response)

    def test_empty_prompt_gpt4_completion(self):
        response = get_gpt4_completion("")
        self.assertIn("success", response)

    # Test very long prompt
    def test_very_long_prompt_gpt_completion(self):
        prompt = "A" * 5000
        response = get_gpt_completion(prompt)
        self.assertIn("error", response)

    def test_very_long_prompt_gpt4_completion(self):
        prompt = "A" * 5000
        response = get_gpt4_completion(prompt)
        self.assertIn("error", response)

    # Test different temperatures for completion
    def test_low_temperature_gpt_completion(self):
        prompt = "What comes after A?"
        response = get_gpt_completion(prompt, temperature=0.1)
        self.assertIsInstance(response, str)

    def test_high_temperature_gpt_completion(self):
        prompt = "What comes after A?"
        response = get_gpt_completion(prompt, temperature=1.0)
        self.assertIsInstance(response, str)

if __name__ == '__main__':
    unittest.main()
