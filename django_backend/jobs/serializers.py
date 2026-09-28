from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import ApplicationModel, JobModel, ResumeModel


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
    resume_link = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationModel
        fields = [
            "id",
            # "job_id",
            # "resume_id",
            "resume_link",
            "score",
            "score_description",
            "cover_letter",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "score", "score_description", "cover_letter", "status"]

    @extend_schema_field(serializers.URLField(allow_null=True))
    def get_resume_link(self, obj):
        if not obj.resume:
            return None
        request = self.context.get("request")
        return obj.resume.get_file_url(request)


class JobSerializer(serializers.ModelSerializer):
    job_applications = ApplicationSerializer(many=True, read_only=True)

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
            "job_applications",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
            "requirements",
            "responsibilities",
            "skills",
            "job_applications",
        ]
