from rest_framework import serializers

from .models import JobModel


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobModel
        fields = ['id', 'title', 'description', 'link', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
