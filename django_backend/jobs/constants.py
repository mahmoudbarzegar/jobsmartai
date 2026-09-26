FIELD_NAMES = ["title", "skills", "requirements", "responsibilities", "description"]
FIELD_WEIGHT_MAP = [
    ("title", "latest_job_title", 0.15),
    ("skills", "skills", 0.40),
    ("requirements", ["education_summary", "years_experience"], 0.20),
    ("responsibilities", "experience_summary", 0.20),
    ("description", "keywords", 0.05),
]

VECTOR_SIZE = 384
