from typing import Any

from .clients import qdrant_client


def ensure_collection(collection_name: str, vectors_config: Any) -> None:
    if not qdrant_client.collection_exists(collection_name):
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=vectors_config,
        )
