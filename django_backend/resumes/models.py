from django.db import models

class Resume(models.Model):
    resume_file = models.FileField(upload_to='resumes/')
    linkedin_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume {self.id} - {self.linkedin_url}"