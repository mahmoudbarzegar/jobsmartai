from django.db import models


class ResumeModel(models.Model):
    file = models.FileField(upload_to='resumes/')
    resume_info = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        # Delete the file from storage
        if self.file:
            self.file.delete(save=False)
        # Delete the model instance
        super().delete(*args, **kwargs)


class JobModel(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    link = models.CharField(max_length=500, null=True)
    resume = models.ForeignKey(ResumeModel, on_delete=models.CASCADE, name='resume')
    score = models.BigIntegerField(null=True, blank=True)
    score_description = models.TextField(null=True, blank=True)
    cover_letter = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
