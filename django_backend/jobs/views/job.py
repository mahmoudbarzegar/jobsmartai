from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from ..models import JobModel, ResumeModel
from ..serializers import JobSerializer
from ..utils import search_jobs_from_remoteok, search_job_from_relocate_me, extract_text_from_pdf
from ..ai_utils import calculate_resume_job_score


@extend_schema(
    tags=["Jobs"]
)
class JobViewSet(viewsets.ModelViewSet):
    http_method_names = ['post']
    model_class = JobModel

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "resume_id": {
                        "type": "integer"
                    }
                },
                "required": ["resume_id"]
            }
        },
    )
    @action(detail=False, methods=['post'], url_path='search')
    def search(self, request, *args, **kwargs):
        resume = ResumeModel.objects.get(id=request.data['resume_id'])
        jobs_from_remote_ok = search_jobs_from_remoteok(skills=resume.resume_info['skills'])
        jobs_from_relocate_me = search_job_from_relocate_me(skills=resume.resume_info['skills'])

        jobs = jobs_from_remote_ok + jobs_from_relocate_me

        for job in jobs:
            try:
                job_object = self.model_class(
                    title=job['title'],
                    description=job['description'],
                    link=job['link'],
                    resume_id=resume.id,
                )
                job_object.save()
            except Exception as e:
                continue

        jobs_created = self.model_class.objects.filter(resume_id=resume.id)
        serializer = JobSerializer(jobs_created, many=True)
        return Response({
            'status': 'success',
            'result': {"jobs": serializer.data}
        }, status=status.HTTP_200_OK)

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "resume_id": {
                        "type": "integer"
                    },
                    "job_id": {
                        "type": "integer"
                    }
                },
                "required": ["resume_id", "job_id"]
            }
        },
    )
    @action(detail=False, methods=['post'], url_path='score')
    def score(self, request, *args, **kwargs):
        resume = ResumeModel.objects.get(id=request.data['resume_id'])
        resume_text = extract_text_from_pdf(resume.file)

        job = JobModel.objects.get(id=request.data['job_id'])
        result = calculate_resume_job_score(resume_text=resume_text, job_description=job.description)

        job.score = result['score']
        job.score_description = result['reason']
        job.save()

        return Response({'status': 'success', 'result': result}, status=status.HTTP_200_OK)
