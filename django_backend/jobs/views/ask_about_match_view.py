from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import JobModel, ResumeModel
from ..serializers import AskAboutMatchRequestSerializer, AskAboutMatchResponseSerializer
from ..vector.ollama import answer_question
from ..vector.rag_vector import ingest_document, is_ingested


class AskAboutMatchView(APIView):
    @extend_schema(
        tags=["ASKAboutMatch"],
        parameters=[
            OpenApiParameter(name="job_id", type=int, location=OpenApiParameter.PATH),
            OpenApiParameter(name="resume_id", type=int, location=OpenApiParameter.PATH),
        ],
        request=AskAboutMatchRequestSerializer,
        responses={200: AskAboutMatchResponseSerializer},
    )
    def post(self, request, resume_id, job_id):
        resume = ResumeModel.objects.get(id=resume_id)
        job = JobModel.objects.get(id=job_id)

        if not is_ingested(resume_id, job_id):
            ingest_document(resume, job)  # runs once per pair

        answer = answer_question(request.data["question"], resume_id, job_id)
        return Response(data={"status": "success", "result": {"answer": answer}}, status=status.HTTP_200_OK)
