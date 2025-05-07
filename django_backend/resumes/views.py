from rest_framework import viewsets
from rest_framework.response import Response


class ResumeViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        return Response({'status': 'success', 'result': 'Resume store successfully'}, status=status.HTTP_200_OK)
