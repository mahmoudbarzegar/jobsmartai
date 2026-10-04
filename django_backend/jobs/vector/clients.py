from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

qdrant_client = QdrantClient(host="localhost", port=6333)
sentence_transformer_model = SentenceTransformer(model_name_or_path="all-MiniLM-L6-v2", device="cpu")
ollama_url = "http://127.0.0.1:11434/api/generate"
