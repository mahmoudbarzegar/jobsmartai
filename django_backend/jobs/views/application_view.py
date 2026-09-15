from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from ..ai_utils import calculate_resume_job_score_description
from ..models import JobModel, ResumeModel
from ..serializers import ApplicationSerializer
from ..utils import get_similarity_score


@extend_schema(tags=["Applications"])
class ApplicationViewSet(viewsets.ModelViewSet):
    http_method_names = ["post"]
    model_class = JobModel
    queryset = model_class.objects.all()
    serializer_class = ApplicationSerializer

    def create(self, request, *args, **kwargs):
        try:
            application_data = request.data
            serializer = self.get_serializer(data=application_data)
            if not serializer.is_valid():
                return Response(
                    {"status": "error", "errorMessage": "Request is not valid", "errors": serializer.errors},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            resume = ResumeModel.objects.get(pk=application_data["resume_id"])
            job = JobModel.objects.get(pk=application_data["job_id"])

            score, breakdown = get_similarity_score(job=job, resume=resume)

            resume_summary = (
                f"{resume.latest_job_title} at {resume.company}, "
                f"{resume.years_experience} years experience. "
                f"Skills: {', '.join(resume.skills)}. {resume.experience_summary}"
            )

            score_description = calculate_resume_job_score_description(
                resume_text=resume_summary, job_description=job.description, score=score
            )

            serializer.save(
                resume=resume,
                job=job,
                score=score,
                score_description=score_description,
            )

            return Response({"status": "success", "result": serializer.data}, status=status.HTTP_201_CREATED)

        except RuntimeError as e:
            return Response({"status": "error", "errorMessage": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"status": "error", "errorMessage": str(e)}, status=status.HTTP_400_BAD_REQUEST)
