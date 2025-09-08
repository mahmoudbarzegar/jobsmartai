from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from ..models import JobModel, ResumeModel
from ..serializers import JobSerializer
from ..utils import search_jobs_from_remoteok, search_job_from_relocate_me, extract_text_from_pdf
from ..ai_utils import calculate_resume_job_score, generate_cover_letter


@extend_schema(
    tags=["Jobs"]
)
class JobViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'get']
    model_class = JobModel
    queryset = model_class.objects.all()
    serializer_class = JobSerializer

    def create(self, request, *args, **kwargs):
        try:
            resume_instance = ResumeModel.objects.get(id=request.data.get('resume_id'))
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'status': 'error', 'errorMessage': 'Request is not valid', 'errors': serializer.errors},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            serializer.save(resume=resume_instance)
            return Response({'status': 'success', 'result': serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'error', 'errorMessage': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
        serializer = self.get_serializer(queryset, many=True)
        return Response({'status': 'success', 'result': {'data': serializer.data}}, status=status.HTTP_200_OK)

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
        try:
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
            serializer = JobSerializer(jobs_created, context={'request': request}, many=True)
            return Response(data={'status': 'success', 'result': {"jobs": serializer.data}}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'status': 'error', 'result': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
    @action(detail=False, methods=['get'], url_path='(?P<job_id>[^/.]+)/score')
    def score(self, request, job_id):
        try:
            job = self.model_class.objects.get(id=job_id)
            resume_text = extract_text_from_pdf(job.resume.file)
            result = calculate_resume_job_score(resume_text=resume_text, job_description=job.description)

            job.score = result['score']
            job.score_description = result['reason']
            job.save()
            return Response({'status': 'success', 'result': result}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'success', 'result': {'score': 0, 'reason': ''}}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='(?P<job_id>[^/.]+)/cover-letter')
    def cover_letter(self, request, job_id):
        try:
            job = self.model_class.objects.get(id=job_id)
            resume_text = extract_text_from_pdf(job.resume.file)
            result = generate_cover_letter(resume_text=resume_text, job_description=job.description)

            job.cover_letter = result
            job.save()

            return Response({'status': 'success', 'result': result}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'success', 'result': str(e)}, status=status.HTTP_200_OK)
