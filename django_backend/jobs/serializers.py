from rest_framework import serializers

from .models import *


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobModel
        fields = ['id', 'title', 'description', 'link', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeModel
        fields = ['id', 'file', 'resume_info', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']