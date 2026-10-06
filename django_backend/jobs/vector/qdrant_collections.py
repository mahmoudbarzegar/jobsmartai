from typing import Any

from .clients import qdrant_client


def ensure_collection(collection_name: str, vectors_config: Any, sparse_vectors_config: Any = None) -> None:
    if qdrant_client.collection_exists(collection_name):
        return

    kwargs = {
        "collection_name": collection_name,
        "vectors_config": vectors_config,
    }

    if sparse_vectors_config is not None:
        kwargs["sparse_vectors_config"] = sparse_vectors_config

    qdrant_client.create_collection(**kwargs)
