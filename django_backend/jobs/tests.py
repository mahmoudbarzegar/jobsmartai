import os

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from django.urls import reverse

from .models import JobModel, ResumeModel


class JobModelTestCase(TestCase):
    def setUp(self):
        resume_file = self.create_file_from_path(os.path.join(os.path.dirname(__file__), 'data/MahmoudBarzegar.pdf'),
                                                 'MahmoudBarzegar.pdf')
        self.resume = ResumeModel.objects.create(
            file=resume_file,
            resume_info={}
        )
        self.API_URL = "http://localhost:8000/api"

    def test_create_job(self):
        """Test creating a JobModel instance with valid data"""
        self.job = JobModel.objects.create(
            title='Software Engineer',
            description='Develop and maintain web applications',
            link='https://example.com/job/software-engineer',
            resume=self.resume,
        )

        # Verify the job was created successfully
        self.assertTrue(isinstance(self.job, JobModel))
        self.assertEqual(self.job.title, 'Software Engineer')
        self.assertEqual(self.job.description, 'Develop and maintain web applications')

        # Verify the job exists in the database
        self.assertEqual(JobModel.objects.count(), 1)
        saved_job = JobModel.objects.get(pk=self.job.pk)
        self.assertEqual(saved_job.title, 'Software Engineer')

    def test_score_job(self):
        self.test_create_job()
        # response = self.client.get(f"{self.API_URL}/jobs/{self.job.id}/score")
        response = self.client.get(reverse('job-score', args=[self.job.id]))
        print(f"Response of score job {response.data['result']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_cover_letter_job(self):
        self.test_create_job()
        response = self.client.get(reverse('job-cover-letter', args=[self.job.id]))
        print(f"Response of score job {response.data['result']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def create_file_from_path(self, file_path, upload_name=None):
        """Helper to create SimpleUploadedFile from file path"""
        if not upload_name:
            upload_name = os.path.basename(file_path)

        with open(file_path, 'rb') as f:
            content = f.read()

        # Guess content type based on extension
        content_type = 'text/plain'
        if file_path.endswith('.pdf'):
            content_type = ' application/pdf'

        return SimpleUploadedFile(upload_name, content, content_type)
