from rest_framework import viewsets, status
from rest_framework.response import Response

from django_backend.resumes.models import ResumeModel
from django_backend.resumes.serializers import ResumeSerializer


class JobViewSet(viewsets.ModelViewSet):
    http_method_names = ['post']
    model_class = ResumeModel
    queryset = ResumeModel.objects.all()
    serializer_class = ResumeSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'status': 'error', 'errorMessage': 'Request is not valid', 'errors': serializer.errors},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            serializer.save()
            return Response({'status': 'success', 'result': serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'error', 'errorMessage': str(e)}, status=status.HTTP_400_BAD_REQUEST)
