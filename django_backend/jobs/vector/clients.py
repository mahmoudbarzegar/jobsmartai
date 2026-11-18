from functools import lru_cache

from django.conf import settings
from fastembed import SparseTextEmbedding
from qdrant_client import QdrantClient
from sentence_transformers import CrossEncoder, SentenceTransformer


@lru_cache
def get_qdrant() -> QdrantClient:
    return QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)


@lru_cache
def get_dense_model() -> SentenceTransformer:
    return SentenceTransformer(settings.EMBED_MODEL, device=settings.AI_DEVICE)


@lru_cache
def get_sparse_model() -> SparseTextEmbedding:
    return SparseTextEmbedding(
        model_name=settings.SPARSE_MODEL,
        cache_dir=settings.FASTEMBED_CACHE,
    )


@lru_cache
def get_reranker() -> CrossEncoder:
    return CrossEncoder(settings.RERANK_MODEL, device=settings.AI_DEVICE)


OLLAMA_URL = settings.OLLAMA_URL
