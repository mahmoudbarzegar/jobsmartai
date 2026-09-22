# jobs/vector_store.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from ..ai_utils import sentence_transformer_model
from ..models import JobModel

client = QdrantClient(host="localhost", port=6333)
VECTOR_SIZE = 384

FIELD_NAMES = ["title", "skills", "requirements", "responsibilities", "description"]


# jobs/vector_store.py
def ensure_job_collection():
    if not client.collection_exists("jobs"):
        client.create_collection(
            collection_name="jobs",
            vectors_config={name: VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE) for name in FIELD_NAMES},
        )


def store_job_vectors(job: JobModel, model=sentence_transformer_model) -> None:
    ensure_job_collection()

    fields_to_embed = {
        "title": job.title,
        "skills": ", ".join(job.skills),
        "requirements": ", ".join(job.requirements) if isinstance(job.requirements, list) else str(job.requirements),
        "responsibilities": ", ".join(job.responsibilities)
        if isinstance(job.responsibilities, list)
        else str(job.responsibilities),
        "description": job.description,
    }

    vectors = {name: model.encode(text).tolist() for name, text in fields_to_embed.items()}

    client.upsert(
        collection_name="jobs",
        points=[PointStruct(id=job.id, vector=vectors, payload={"job_id": job.id})],
    )
