from rest_framework import serializers

from .models import JobModel, ResumeModel


class JobSerializer(serializers.ModelSerializer):
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = JobModel
        fields = [
            "id",
            "title",
            "description",
            "link",
            "resume_url",
            "score",
            "score_description",
            "created_at",
            "updated_at",
            "cover_letter",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_resume_url(self, obj):
        if obj.resume and obj.resume.file:  # assuming Resume has 'file' attribute
            request = self.context.get("request")
            if request is None:
                return obj.resume.file.url  # fallback: relative URL instead of absolute
            return request.build_absolute_uri(obj.resume.file.url)
        return None


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
