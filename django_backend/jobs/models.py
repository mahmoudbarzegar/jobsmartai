from django.db import models


class JobModel(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    link = models.CharField(max_length=500)
    resume_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['resume_id'])
        ]
