from rest_framework import serializers

from .models import *


class JobSerializer(serializers.ModelSerializer):
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = JobModel
        fields = ['id', 'title', 'description', 'link', 'resume_url', 'score', 'score_description', 'created_at',
                  'updated_at', 'cover_letter']
        read_only_fields = ['created_at', 'updated_at']

    def get_resume_url(self, obj):
        if obj.resume and obj.resume.file:  # assuming Resume has 'file' attribute
            request = self.context.get('request')
            return request.build_absolute_uri(obj.resume.file.url)
        return None


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeModel
        fields = ['id', 'file', 'resume_info', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
