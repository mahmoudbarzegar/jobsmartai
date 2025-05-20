from rest_framework import serializers

from .models import ResumeModel


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeModel
        fields = ['id', 'file', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
