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