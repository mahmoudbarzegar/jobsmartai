# jobs/vector_store.py
from qdrant_client.models import Distance, VectorParams

from ..constants import FIELD_NAMES, VECTOR_SIZE
from .clients import qdrant_client


def ensure_collection(collection_name: str):
    if not qdrant_client.collection_exists(collection_name):
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config={name: VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE) for name in FIELD_NAMES},
        )
