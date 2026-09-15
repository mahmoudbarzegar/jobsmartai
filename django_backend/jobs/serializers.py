from rest_framework import serializers

from .models import ApplicationModel, JobModel, ResumeModel


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


class ApplicationSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(source="job", queryset=JobModel.objects.all())
    resume_id = serializers.PrimaryKeyRelatedField(source="resume", queryset=ResumeModel.objects.all())

    class Meta:
        model = ApplicationModel
        fields = [
            "id",
            "job_id",
            "resume_id",
            "score",
            "score_description",
            "cover_letter",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "score", "score_description", "cover_letter", "status"]
