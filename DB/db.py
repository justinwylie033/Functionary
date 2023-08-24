import uuid
from decouple import config
import pinecone
from tenacity import retry, wait_random_exponential, stop_after_attempt
import openai


class FunctionaryDB:
    INDEX_NAME = 'functionary'
    METADATA_CONFIG = {"indexed": ["code", "efficiency", "output"]}

    def __init__(self):
        self.api_key = config('PINECONE_API_KEY')
        self.openai_api_key = config('OPEN_AI_KEY')
        self.env = config('PINECONE_ENV')
        self._initialize_pinecone(self.api_key, self.env)  # <-- Fix is here, pass the parameters
        self.index = self._setup_index()

    @staticmethod
    def _initialize_pinecone(api_key, env):
        pinecone.init(api_key=api_key, environment=env)

    @staticmethod
    def _setup_index():
        if FunctionaryDB.INDEX_NAME not in pinecone.list_indexes():
            pinecone.create_index(FunctionaryDB.INDEX_NAME, dimension=1536, metadata_config=FunctionaryDB.METADATA_CONFIG)
        return pinecone.Index(FunctionaryDB.INDEX_NAME)

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def _get_embedding(self, code, model="text-embedding-ada-002"):
        openai.api_key = self.openai_api_key
        response = openai.Embedding.create(input=code, model=model)
        return response['data'][0]['embedding']
    

    def function_exists(self, code, efficiency=None, output=None):
        existing_functions = self.query_data(code=code, efficiency=efficiency, output=output)
        return bool(existing_functions)


    def upsert_functions(self, code, efficiency=None, output=None):
        if self.function_exists(code, efficiency, output):
            print(f"Function with code: {code} already exists. Skipping upsert.")
            return
        embedding = self._get_embedding(code)
        item_id = str(uuid.uuid4())
        metadata = {
            "code": code,
            "efficiency": efficiency,
            "output": output
        }
        self.index.upsert([(item_id, embedding, metadata)])


    def query_data(self, code=None, efficiency=None, output=None, top_k=6):
        if code:
            embedding = self._get_embedding(code)
            results = self.index.query(embedding, top_k=top_k, include_metadata=True)
        elif efficiency or output:
            # If the query is based on efficiency or output, we need a mechanism to generate embeddings for them.
            # For demonstration purposes, I'm assuming that generating embeddings for efficiency or output is valid.
            # You might need to adjust this based on what's logically correct for your application.
            
            # Using code as primary, if not present then efficiency, and lastly output
            query_string = code or efficiency or output
            embedding = self._get_embedding(query_string)
            results = self.index.query(embedding, top_k=top_k, include_metadata=True)
        else:
            # If no parameters are given, just return an empty list (or you can handle this differently based on your requirements)
            return []

        # Filter the results based on given metadata
        filtered_results = [match for match in results['matches']
                            if (not code or match['metadata']['code'] == code) and
                            (not efficiency or match['metadata']['efficiency'] == efficiency) and
                            (not output or match['metadata']['output'] == output)]

        return [(match['metadata']['code'], match['metadata']['efficiency'], match['metadata']['output']) for match in filtered_results[:top_k]]

def main():
    # Initialize the FunctionaryDB
    db = FunctionaryDB()

    # Upsert some sample functions into the database
    sample_code_1 = "def hello(): return 'hello'"
    sample_efficiency_1 = "O(1)"
    sample_output_1 = "hello"
    db.upsert_functions(sample_code_1, sample_efficiency_1, sample_output_1)

    sample_code_2 = "def add(a, b): return a + b"
    sample_efficiency_2 = "O(1)"
    sample_output_2 = "a+b"
    db.upsert_functions(sample_code_2, sample_efficiency_2, sample_output_2)

    # Query for a function based on code
    results_code = db.query_data(code="def hello(): return 'hello'")
    print("Results for code query:")
    for result in results_code:
        print(result)

    # Query for a function based on efficiency
    results_efficiency = db.query_data(efficiency="O(1)")
    print("\nResults for efficiency query:")
    for result in results_efficiency:
        print(result)

    # Query for a function based on output
    results_output = db.query_data(output="a+b")
    print("\nResults for output query:")
    for result in results_output:
        print(result)


if __name__ == "__main__":
    main()
