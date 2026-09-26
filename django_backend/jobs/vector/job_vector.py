from qdrant_client.models import PointStruct

from ..ai_utils import sentence_transformer_model
from ..models import JobModel
from .clients import qdrant_client
from .qdrant_collections import ensure_collection


def store_job_vectors(job: JobModel) -> None:
    ensure_collection(collection_name="jobs")

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
