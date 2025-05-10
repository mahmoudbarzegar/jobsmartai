from rest_framework import serializers


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
