from django.db import models


class BaseModel(models.Model):  # noqa: DJ008
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ResumeModel(BaseModel):
    file = models.FileField(upload_to="resumes/")
    resume_info = models.JSONField(default=dict)

    def __str__(self):
        return self.file.name

    def delete(self, *args, **kwargs):
        # Delete the file from storage
        if self.file:
            self.file.delete(save=False)
        # Delete the model instance
        super().delete(*args, **kwargs)


class JobModel(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    link = models.URLField(max_length=500, default="", blank=True)
    skill = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title


class Status(models.TextChoices):
    APPLIED = "applied", "Applied"
    REVIEWED = "reviewed", "Reviewed"
    REJECTED = "rejected", "Rejected"
    HIRED = "hired", "Hired"


class ApplicationModel(BaseModel):
    resume = models.ForeignKey(ResumeModel, on_delete=models.CASCADE)
    job = models.ForeignKey(JobModel, on_delete=models.CASCADE)
    score = models.SmallIntegerField(null=True, blank=True)
    score_description = models.TextField(default="", blank=True)
    cover_letter = models.TextField(default="", blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.APPLIED)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["resume", "job"], name="unique_resume_job_application")]

    def __str__(self):
        return f"{self.resume} → {self.job} ({self.status})"
