from django.db import models

class ResumeModel(models.Model):
    file = models.FileField(upload_to='resumes/')
    linkedin_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume {self.id} - {self.linkedin_url}"

    def delete(self, *args, **kwargs):
        # Delete the file from storage
        if self.file:
            self.file.delete(save=False)
        # Delete the model instance
        super().delete(*args, **kwargs)