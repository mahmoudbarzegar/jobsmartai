import uuid
from typing import Any

from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchText,
    MatchValue,
    PointStruct,
    VectorParams,
)

from ..models import JobModel, ResumeModel
from .clients import sentence_transformer_model
from .qdrant_collections import ensure_collection, qdrant_client


def ingest_resume(resume: ResumeModel) -> None:
    text = (
        f"Resume Description: {', '.join(resume.keywords)} Skills: {', '.join(resume.skills)}. "
        f"Requirements: {resume.education_summary} {resume.years_experience} "
        f"Responsibilities: {resume.experience_summary}"
    )
    _store_chunks(
        text,
        payload={
            "resume_id": resume.id,
            "skills": ", ".join(resume.skills),
            "requirements": f"{resume.education_summary} {resume.years_experience}",
            "responsibilities": resume.experience_summary,
            "description": ", ".join(resume.keywords),
            "type": "resume",
        },
    )


def ingest_job(job: JobModel) -> None:
    text = (
        f"Job Description: {job.description} Skills: {', '.join(job.skills)}. Requirements: {job.requirements} "
        f"Responsibilities: {job.responsibilities}"
    )
    _store_chunks(
        text,
        payload={
            "job_id": job.id,
            "skills": ", ".join(job.skills),
            "requirements": job.requirements,
            "responsibilities": job.responsibilities,
            "description": job.description,
            "type": "job",
        },
    )


def _store_chunks(text: str, payload: dict) -> None:
    ensure_collection(collection_name="rag_chunks", vectors_config=VectorParams(size=384, distance=Distance.COSINE))
    chunks = _chunk_text(text)
    points = []
    for chunk in chunks:
        vector = sentence_transformer_model.encode(chunk).tolist()
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text": chunk, **payload},
            )
        )

    qdrant_client.upsert(collection_name="rag_chunks", points=points)


def delete_rag_chunks(resume_id: int | None = None, job_id: int | None = None):
    conditions = []
    if resume_id:
        conditions.append(FieldCondition(key="resume_id", match=MatchValue(value=resume_id)))
    if job_id:
        conditions.append(FieldCondition(key="job_id", match=MatchValue(value=job_id)))

    qdrant_client.delete(
        collection_name="rag_chunks",
        points_selector=Filter(must=conditions),
    )


def is_ingested(resume_id: int, job_id: int) -> bool:
    ensure_collection(collection_name="rag_chunks", vectors_config={VectorParams(size=384, distance=Distance.COSINE)})

    count = qdrant_client.count(
        collection_name="rag_chunks",
        count_filter=Filter(
            must=[
                FieldCondition(key="resume_id", match=MatchValue(value=resume_id)),
                FieldCondition(key="job_id", match=MatchValue(value=job_id)),
            ]
        ),
    ).count
    return count > 0


def retrieve_chunks(
    question: str,
    resume_id: int,
    job_id: int,
    resume_filters: dict[str, str],
    job_filters: dict[str, str],
    top_k: int = 5,
) -> list[str]:
    question_vector = sentence_transformer_model.encode(question).tolist()

    resume_must_conditions = [
        FieldCondition(key="resume_id", match=MatchValue(value=resume_id)),
    ]
    resume_hits = _get_hits(question_vector, resume_must_conditions, resume_filters, top_k * 2)

    job_must_conditions = [
        FieldCondition(key="job_id", match=MatchValue(value=job_id)),
    ]
    job_hits = _get_hits(question_vector, job_must_conditions, job_filters, top_k * 2)

    all_hits = resume_hits + job_hits
    all_hits.sort(key=lambda h: h.score, reverse=True)

    # return [h.payload["text"] for h in resume_hits] + [h.payload["text"] for h in job_hits]

    seen = set()
    unique_chunks = []
    for hit in all_hits:
        text = hit.payload["text"]
        if text not in seen:
            seen.add(text)
            unique_chunks.append(text)
        if len(unique_chunks) >= top_k:
            break

    return unique_chunks


def _get_hits(question_vector: Any, must_conditions: list, filters: dict[str, str], top_k: int = 5) -> Any:
    filters = filters or {}

    if "skills" in filters:
        must_conditions.append(FieldCondition(key="skills", match=MatchText(text=filters["skills"])))

    if "requirements" in filters:
        must_conditions.append(FieldCondition(key="requirements", match=MatchText(text=filters["requirements"])))

    if "responsibilities" in filters:
        must_conditions.append(
            FieldCondition(key="responsibilities", match=MatchText(text=filters["responsibilities"]))
        )

    if "description" in filters:
        must_conditions.append(FieldCondition(key="description", match=MatchText(text=filters["description"])))

    return qdrant_client.query_points(
        collection_name="rag_chunks",
        query=question_vector,
        query_filter=Filter(must=must_conditions),
        # limit=top_k,
    ).points


def _chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i : i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks
