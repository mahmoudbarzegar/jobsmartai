# jobs/vector_store.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from ..ai_utils import sentence_transformer_model
from ..models import ResumeModel

client = QdrantClient(host="localhost", port=6333)
VECTOR_SIZE = 384

FIELD_NAMES = ["title", "skills", "requirements", "responsibilities", "description"]


def ensure_resume_collection():
    if not client.collection_exists("resumes"):
        client.create_collection(
            collection_name="resumes",
            vectors_config={name: VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE) for name in FIELD_NAMES},
        )


def store_resume_vectors(resume: ResumeModel) -> None:
    ensure_resume_collection()

    fields_to_embed = {
        "title": resume.latest_job_title,
        "skills": ", ".join(resume.skills),
        "requirements": f"{resume.education_summary} {resume.years_experience}",
        "responsibilities": resume.experience_summary,
        "description": ", ".join(resume.keywords),
    }

    vectors = {name: sentence_transformer_model.encode(text).tolist() for name, text in fields_to_embed.items()}

    client.upsert(
        collection_name="resumes",
        points=[PointStruct(id=resume.id, vector=vectors, payload={"resume_id": resume.id})],
    )
