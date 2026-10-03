from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..constants import FIELD_WEIGHT_MAP
from ..models import ApplicationModel, JobModel, ResumeModel
from ..serializers import ApplicationSerializer
from ..vector.clients import qdrant_client
from ..vector.job_vector import store_job_vectors
from ..vector.ollama import sentence_transformer_model
from ..vector.resume_vector import store_resume_vectors


class FindBestResumes(APIView):
    serializer_class = ApplicationSerializer

    @extend_schema(
        tags=["FindBestResumes"],
        parameters=[
            OpenApiParameter(name="job_id", type=int, location=OpenApiParameter.PATH),
        ],
        responses=serializer_class,
    )
    def get(self, request, job_id):
        try:
            job = JobModel.objects.get(pk=job_id)
        except JobModel.DoesNotExist:
            return Response(
                {"status": "error", "errorMessage": "Job not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            store_job_vectors(job=job)

            for resume in ResumeModel.objects.all():
                store_resume_vectors(resume)

            job_fields = {
                "title": job.title,
                "skills": ", ".join(job.skills),
                "requirements": job.requirements,
                "responsibilities": job.responsibilities,
                "description": job.description,
            }

            field_scores_per_resume = {}

            for field_name in job_fields:
                job_vector = sentence_transformer_model.encode(job_fields[field_name]).tolist()

                hits = qdrant_client.query_points(
                    collection_name="resumes",
                    query=job_vector,
                    using=field_name,
                    limit=50,
                ).points

                for hit in hits:
                    field_scores_per_resume.setdefault(hit.id, {})[field_name] = hit.score

            if not field_scores_per_resume:
                return Response({"status": "success", "job_id": job_id, "matches": []})

            candidate_resumes = ResumeModel.objects.filter(id__in=field_scores_per_resume.keys())

            ranked = []
            for resume in candidate_resumes:
                total_score = 0

                for field, _, weight in FIELD_WEIGHT_MAP:
                    total_score += field_scores_per_resume[resume.id][field] * weight

                ranked.append(
                    {
                        "resume_id": resume.id,
                        "resume_link": resume.get_file_url(request),
                        "score": round(total_score * 100, 2),
                        "breakdown": field_scores_per_resume[resume.id],
                    }
                )

                ApplicationModel.objects.update_or_create(
                    resume=resume,
                    job=job,
                    defaults={"score": total_score},
                )

            ranked.sort(key=lambda r: r["score"], reverse=True)
            return Response({"status": "success", "result": ranked}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"status:": "error", "error_message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
