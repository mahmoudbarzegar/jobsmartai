# jobs/vector_store.py
from qdrant_client.models import PointStruct

from ..ai_utils import sentence_transformer_model
from ..models import ResumeModel
from .clients import qdrant_client
from .qdrant_collections import ensure_collection


def store_resume_vectors(resume: ResumeModel) -> None:
    ensure_collection(collection_name="resumes")

    fields_to_embed = {
        "title": resume.latest_job_title,
        "skills": ", ".join(resume.skills),
        "requirements": f"{resume.education_summary} {resume.years_experience}",
        "responsibilities": resume.experience_summary,
        "description": ", ".join(resume.keywords),
    }

    vectors = {name: sentence_transformer_model.encode(text).tolist() for name, text in fields_to_embed.items()}

    qdrant_client.upsert(
        collection_name="resumes",
        points=[PointStruct(id=resume.id, vector=vectors, payload={"resume_id": resume.id})],
    )
