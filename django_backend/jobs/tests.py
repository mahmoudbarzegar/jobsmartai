import os

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import JobModel, ResumeModel


class JobModelTestCase(TestCase):
    def setUp(self):
        resume_file = self.create_file_from_path(os.path.join(os.path.dirname(__file__), 'data/MahmoudBarzegar.pdf'),
                                                 'MahmoudBarzegar.pdf')
        self.resume = ResumeModel.objects.create(
            file=resume_file,
            resume_info={}
        )

    def test_job_creation(self):
        print(f"Here {os.path.join(os.path.dirname(__file__), 'data/MahmoudBarzegar.pdf')}")

        """Test creating a JobModel instance with valid data"""
        job = JobModel.objects.create(
            title='Software Engineer',
            description='Develop and maintain web applications',
            link='https://example.com/job/software-engineer',
            resume=self.resume,

        )

        print(f"Here {job.id}")

        # Verify the job was created successfully
        self.assertTrue(isinstance(job, JobModel))
        self.assertEqual(job.title, 'Software Engineer')
        self.assertEqual(job.description, 'Develop and maintain web applications')

        # Verify the job exists in the database
        self.assertEqual(JobModel.objects.count(), 1)
        saved_job = JobModel.objects.get(pk=job.pk)
        self.assertEqual(saved_job.title, 'Software Engineer')

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
