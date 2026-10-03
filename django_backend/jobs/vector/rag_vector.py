import uuid

from qdrant_client.models import Distance, FieldCondition, Filter, MatchValue, PointStruct, VectorParams

from ..models import JobModel, ResumeModel
from .clients import sentence_transformer_model
from .qdrant_collections import ensure_collection, qdrant_client


def ingest_document(resume: ResumeModel, job: JobModel) -> None:
    ensure_collection(collection_name="rag_chunks", vectors_config=VectorParams(size=384, distance=Distance.COSINE))

    full_text = f"""
    Resume:
    {resume.experience_summary} Skills: {', '.join(resume.skills)}. Education: {resume.education_summary}.

    Job Description:
    {job.description}
    """

    chunks = _chunk_text(full_text)
    points = []
    for chunk in chunks:
        vector = sentence_transformer_model.encode(chunk).tolist()
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text": chunk, "resume_id": resume.id, "job_id": job.id},
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
    ensure_collection("rag_chunks", vectors_config=VectorParams(size=384, distance=Distance.COSINE))
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


def retrieve_chunks(question: str, resume_id: int, job_id: int, top_k: int = 5) -> list[str]:
    question_vector = sentence_transformer_model.encode(question).tolist()

    hits = qdrant_client.query_points(
        collection_name="rag_chunks",
        query=question_vector,
        query_filter=Filter(
            must=[
                FieldCondition(key="resume_id", match=MatchValue(value=resume_id)),
                FieldCondition(key="job_id", match=MatchValue(value=job_id)),
            ]
        ),
        limit=top_k,
    ).points

    return [hit.payload["text"] for hit in hits]


def _chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i : i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks
