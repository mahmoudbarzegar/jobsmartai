from qdrant_client.models import Distance, PointStruct, VectorParams

from ..constants import FIELD_NAMES, VECTOR_SIZE
from ..models import JobModel
from .clients import qdrant_client
from .ollama import sentence_transformer_model
from .qdrant_collections import ensure_collection


def store_job_vectors(job: JobModel) -> None:
    ensure_collection(
        collection_name="jobs",
        vectors_config={name: VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE) for name in FIELD_NAMES},
    )

    fields_to_embed = {
        "title": job.title,
        "skills": ", ".join(job.skills),
        "requirements": ", ".join(job.requirements) if isinstance(job.requirements, list) else str(job.requirements),
        "responsibilities": ", ".join(job.responsibilities)
        if isinstance(job.responsibilities, list)
        else str(job.responsibilities),
        "description": job.description,
    }

    vectors = {name: sentence_transformer_model.encode(text).tolist() for name, text in fields_to_embed.items()}

    qdrant_client.upsert(
        collection_name="jobs",
        points=[PointStruct(id=job.id, vector=vectors, payload={"job_id": job.id})],
    )
