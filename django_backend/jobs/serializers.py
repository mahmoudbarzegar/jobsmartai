from rest_framework import serializers

from .models import JobModel, ResumeModel


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobModel
        fields = [
            "id",
            "title",
            "description",
            "link",
            "requirements",
            "responsibilities",
            "skills",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "requirements", "responsibilities", "skills"]


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeModel
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "latest_job_title",
            "company",
            "years_experience",
            "skills",
            "keywords",
            "file",
            "education_summary",
            "experience_summary",
            "resume_info_raw",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "full_name",
            "email",
            "phone",
            "latest_job_title",
            "company",
            "years_experience",
            "skills",
            "keywords",
            "education_summary",
            "experience_summary",
            "resume_info_raw",
            "created_at",
            "updated_at",
        ]
