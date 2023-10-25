import uuid
from typing import List, Tuple, Optional, Dict, Union
from decouple import config
import pinecone
from tenacity import retry, wait_random_exponential, stop_after_attempt
import openai

class FunctionaryDB:
    """
    Handles operations related to managing code data in a Pinecone index.
    """
    
    INDEX_NAME = 'functionary'
    METADATA_CONFIG = {"indexed": ["code", "efficiency", "output", "description"]}

    def __init__(self) -> None:
        self.api_key = config('PINECONE_API_KEY')
        self.openai_api_key = config('OPEN_AI_KEY')
        self.env = config('PINECONE_ENV')
        self._initialise_pinecone(self.api_key, self.env)
        self.index = self._setup_index()

    @staticmethod
    def _initialise_pinecone(api_key: str, env: str) -> None:
        pinecone.init(api_key=api_key, environment=env)

    @staticmethod
    def _setup_index() -> pinecone.Index:
        if FunctionaryDB.INDEX_NAME not in pinecone.list_indexes():
            pinecone.create_index(FunctionaryDB.INDEX_NAME, dimension=1536, 
                                  metadata_config=FunctionaryDB.METADATA_CONFIG)
        return pinecone.Index(FunctionaryDB.INDEX_NAME)

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def _get_embedding(self, code: str, model: str = "text-embedding-ada-002") -> List[float]:
        openai.api_key = self.openai_api_key
        response = openai.Embedding.create(input=code, model=model)
        return response['data'][0]['embedding']


    def upsert_functions(self, code: str, efficiency: Optional[str] = None, 
                        output: Optional[str] = None, description: Optional[str] = None) -> None:
        if self.function_exists(code, efficiency, output, description):
            print(f"Function with code: {code} already exists. Skipping upsert.")
            return
        embedding = self._get_embedding(code)
        item_id = str(uuid.uuid4())
        metadata = {
            "code": code,
            "efficiency": efficiency,
            "output": output,
            "description": description
        }
        self.index.upsert([(item_id, embedding, metadata)])

    def function_exists(self, code: str, efficiency: Optional[str] = None, 
                        output: Optional[str] = None, description: Optional[str] = None) -> bool:
        existing_functions = self.query_data(code=code, efficiency=efficiency, output=output, description=description)
        return bool(existing_functions)



    def query_data(self, code: Optional[str] = None, efficiency: Optional[str] = None, 
                output: Optional[str] = None, description: Optional[str] = None, 
                top_k: int = 6) -> List[Tuple[str, Optional[str], Optional[str], Optional[str]]]:
        """Queries the database for functions based on given attributes."""

        if code:
            embedding = self._get_embedding(code)
            results = self.index.query(embedding, top_k=top_k * 10, include_metadata=True)
        else:
            embedding = [0.0] * 1536
            results = self.index.query(embedding, top_k=500, include_metadata=True)

        filtered_results = [
            match for match in results['matches']
            if (not code or match['metadata']['code'] == code) and
            (not efficiency or match['metadata']['efficiency'] == efficiency) and
            (not output or match['metadata']['output'] == output) and
            (not description or match['metadata']['description'] == description)
        ]

        return [(match['metadata']['code'], match['metadata']['efficiency'], 
                match['metadata']['output'], match['metadata']['description']) 
                for match in filtered_results[:top_k]]



def main() -> None:
    db = FunctionaryDB()

    # Upsert example functions
    db.upsert_functions("def hello(): return 'hello'", "O(1)", "hello")
    db.upsert_functions("def add(a, b): return a + b", "O(1)", "a+b")

    # Query functions
    results_code = db.query_data(code="def hello(): return 'hello'")
    print("\nResults for code query:")
    for result in results_code:
        print(result)

    results_efficiency = db.query_data(efficiency="O(1)")
    print("\nResults for efficiency query:")
    for result in results_efficiency:
        print(result)

    results_output = db.query_data(output="a+b")
    print("\nResults for output query:")
    for result in results_output:
        print(result)

if __name__ == "__main__":
    main()
