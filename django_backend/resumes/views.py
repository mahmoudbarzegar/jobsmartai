from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.parsers import MultiPartParser, FormParser

from .models import ResumeModel
from .serializers import ResumeSerializer


class ResumeViewSet(viewsets.ModelViewSet):
    http_method_names = ['post']
    model_class = ResumeModel
    queryset = model_class.objects.all()
    serializer_class = ResumeSerializer
    parser_classes = [MultiPartParser, FormParser]  # Important for file uploads

    @extend_schema(
        request={
            'multipart/form-data': ResumeSerializer
        },
        parameters=[
            OpenApiParameter(
                name='resume_file',
                type=OpenApiTypes.BINARY,
                required=True,
                description="Resume file to upload",
                style='form'
            ),
        ],
        operation_id="upload_resume",
        description="Upload resume file and LinkedIn URL"
    )
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
