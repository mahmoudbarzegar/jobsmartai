# jobs/vector_store.py
from qdrant_client.models import Distance, PointStruct, VectorParams

from ..constants import FIELD_NAMES, VECTOR_SIZE
from ..models import ResumeModel
from .clients import get_dense_model, get_qdrant
from .qdrant_collections import ensure_collection


def store_resume_vectors(resume: ResumeModel) -> None:
    ensure_collection(
        collection_name="resumes",
        vectors_config={name: VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE) for name in FIELD_NAMES},
    )

    fields_to_embed = {
        "title": resume.latest_job_title,
        "skills": ", ".join(resume.skills),
        "requirements": f"{resume.education_summary} {resume.years_experience}",
        "responsibilities": resume.experience_summary,
        "description": ", ".join(resume.keywords),
    }

    vectors = {name: get_dense_model().encode(text).tolist() for name, text in fields_to_embed.items()}

    get_qdrant().upsert(
        collection_name="resumes",
        points=[PointStruct(id=resume.id, vector=vectors, payload={"resume_id": resume.id})],
    )
