from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from ..constants import FIELD_NAMES, VECTOR_SIZE

qdrant_client = QdrantClient(host="localhost", port=6333)


def ensure_collection(collection_name: str):
    if not qdrant_client.collection_exists(collection_name):
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config={name: VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE) for name in FIELD_NAMES},
        )
