import uuid
from decouple import config
import pinecone
from tqdm import tqdm
from tenacity import retry, wait_random_exponential, stop_after_attempt
import openai
from nltk.tokenize import sent_tokenize


class FunctionaryDB:
    def __init__(self):
        self.api_key = config('PINECONE_API_KEY')
        self.openai_api_key=config('OPEN_AI_KEY')
        self.env = config('PINECONE_ENV')
        self._initialize_pinecone()
        self.index = self._setup_index()


    def _initialize_pinecone(self):
        import nltk
        nltk.download('punkt')

        """Initialize the Pinecone service."""
        pinecone.init(api_key=self.api_key, environment=self.env)

    def _setup_index(self):
        """Setup the Pinecone index."""
        index_name = 'functionary'
        if index_name not in pinecone.list_indexes():
            metadata_config = {"indexed": ["info", "status", "code", "efficiency"]}
            pinecone.create_index(index_name, dimension=1536, metadata_config=metadata_config)
        
        return pinecone.Index(index_name)

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def _get_embedding(self, text, model="text-embedding-ada-002"):
        """Generate embedding for a given text."""
        openai.api_key=self.openai_api_key
        response = openai.Embedding.create(input=text, model=model)
        return response['data'][0]['embedding']

    def _merge_sentences(self, sentences, window=10, stride=2):
        """Merge sentences to form a longer context."""
        merged = []
        for i in tqdm(range(0, len(sentences), stride)):
            i_end = min(len(sentences) - 1, i + window)
            merged.append(' '.join(sentences[i:i_end]))
        return merged

    def _upsert_to_pinecone(self, items, metadata_list=None):  
        """Insert or update items and their embeddings into Pinecone with metadata."""
        embeddings = [self._get_embedding(item) for item in items]
        for idx, (item, embedding) in enumerate(zip(items, embeddings)):
            item_id = str(uuid.uuid4())
            print(f"Upserting item {item_id} with text: {item}")
            metadata = {"text": item}
            if metadata_list and idx < len(metadata_list):
                metadata.update(metadata_list[idx])
            self.index.upsert([(item_id, embedding, metadata)])

    def upsert_code_with_metadata(self, code, metadata):
        """Insert or update code and its metadata into Pinecone."""
        self._upsert_to_pinecone([code], [metadata])

    def upsert_functions(self, functions, metadata_list=None):
        """Insert or update functions and their embeddings into Pinecone with metadata."""
        if metadata_list and len(functions) != len(metadata_list):
            raise ValueError("The length of functions and metadata_list must match.")
        
        print("Upserting functions into Pinecone")
        self._upsert_to_pinecone(functions, metadata_list)


    def upsert_data(self, data):
        """Insert or update sentences and their embeddings into Pinecone."""
        sentences = sent_tokenize(data)
        merged_sentences = self._merge_sentences(sentences)
        self._upsert_to_pinecone(merged_sentences)

    def query_data(self, query, top_k=6):
        """Query the Pinecone index and return relevant matches."""
        print(f"Query: {query}")
        embedding = self._get_embedding(query)
        results = self.index.query(embedding, top_k=top_k, include_metadata=True)
        
        matches = []
        for match in results['matches']:
            text = match['metadata']['text']
            efficiency = match['metadata'].get('efficiency', 'N/A')  # Gets the efficiency value, or 'N/A' if not found
            matches.append((text, efficiency))

        return matches



if __name__ == "__main__":
    # Initialize the FunctionaryDB
    db = FunctionaryDB()

    # Insert or update sample data
    sample_data = "Your sample data here."
    db.upsert_data(sample_data)

    # Insert or update sample functions with efficiency metadata
    sample_functions = ["def add(a, b): return a + b"]
    sample_metadata = [{"efficiency": 0.95}]  # 0.95 represents the efficiency of the function, can be any value between 0 and 1
    db.upsert_functions(sample_functions, sample_metadata)

    # Query the database
    query_results = db.query_data("password cracker algorithm")
    
    for text, efficiency in query_results:
        print(f"Text: {text}\nEfficiency: {efficiency}\n")
