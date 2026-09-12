from pydantic import BaseModel


class ResumeInfo(BaseModel):
    full_name: str
    email: str | None = None
    phone: str | None = None
    skills: list[str]
    latest_job_title: str
    company: str
    years_experience: float
    education_summary: str
    keywords: list[str]
    experience_summary: str


class JobInfo(BaseModel):
    requirements: str | None = None
    skills: list[str]
    responsibilities: str
