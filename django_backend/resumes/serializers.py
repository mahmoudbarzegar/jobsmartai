from rest_framework import serializers

from .models import ResumeModel


class ResumeSerializer(serializers.ModelSerializer):

    linkedin_url = serializers.URLField(
        help_text="LinkedIn profile URL"
    )

    class Meta:
        model = ResumeModel
        fields = ['resume_file', 'linkedin_url']
        read_only_fields = ['created_at', 'updated_at']
