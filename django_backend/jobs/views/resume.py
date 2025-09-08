from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FormParser

from ..models import ResumeModel
from ..serializers import ResumeSerializer
from ..ai_utils import analyze_resume_with_ollama
from ..utils import extract_text_from_pdf


@extend_schema(
    tags=["Resume"]
)
class ResumeViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'delete']
    model_class = ResumeModel
    queryset = model_class.objects.all()
    serializer_class = ResumeSerializer
    parser_classes = [MultiPartParser, FormParser]  # Important for file uploads

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary"
                    }
                },
                "required": ["file"]
            }
        },
    )
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'status': 'error', 'error_message': 'Request is not valid', 'errors': serializer.errors},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            resume_text = extract_text_from_pdf(request.data['file'])
            analyze_resume_text = analyze_resume_with_ollama(resume_text)

            serializer.save(resume_info=analyze_resume_text)
            return Response({'status': 'success', 'result': serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'error', 'error_message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'status': 'success', 'result': {'data': serializer.data}}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response({'status': 'success', 'result': 'Resume deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status:': 'error', 'error_message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
