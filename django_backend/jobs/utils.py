import fitz
import requests
from bs4 import BeautifulSoup

from .ai_utils import calculate_similarity_score
from .models import JobModel, ResumeModel


def search_jobs_from_remoteok(skills: list):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/112.0.0.0 Safari/537.36"}
        search_keywords = skills[:1]
        query = "+".join(search_keywords)
        url = f"https://remoteok.com/api?tags={query}"
        response = requests.get(url, headers=headers, timeout=300)
        if response.status_code == 200:
            return [
                {"title": job["position"], "link": job["url"], "description": job["description"]}
                for job in response.json()[1:]
            ]
        return {}
    except Exception:
        return {}


def search_job_from_relocate_me(skills: list):
    try:
        search_keywords = skills[:1]
        query = "+".join(search_keywords)
        url = f"https://relocate.me/international-jobs?query={query}"
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/112.0.0.0 Safari/537.36"}
        result = requests.get(url, headers=headers, timeout=300)
        soup = BeautifulSoup(result.text, "html.parser")

        jobs = []
        for card in soup.select(".job__title"):
            title_tag = card.select_one(".job__title b")
            link_tag = card.select_one(".job__title a")
            url_suffix = link_tag["href"] if link_tag else ""

            job_url = "https://relocate.me" + url_suffix
            job_result = requests.get(job_url, headers=headers, timeout=300)
            soup = BeautifulSoup(job_result.text, "html.parser")
            description_block = soup.select_one(".job-info__description")  # may vary

            jobs.append(
                {
                    "title": title_tag.text.strip() if title_tag else "N/A",
                    "link": job_url,
                    "description": description_block.get_text(separator="\n").strip()
                    if description_block
                    else "No job description found.",
                }
            )
        return jobs

    except Exception:
        return {}


def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        result = page.get_text()
        if isinstance(result, str):
            text += result
    return text


def get_similarity_score(resume: ResumeModel, job: JobModel) -> tuple[float, dict]:
    total_score = 0
    breakdown = {}

    field_pairs = [
        ("title", "latest_job_title", 0.15),
        ("skills", "skills", 0.40),
        ("requirements", ["education_summary", "years_experience"], 0.20),
        ("responsibilities", "experience_summary", 0.20),
        ("description", "keywords", 0.05),
    ]

    for job_field, resume_field, weight in field_pairs:
        job_value = getattr(job, job_field)

        if isinstance(resume_field, list):
            resume_value = " ".join(str(getattr(resume, f)) for f in resume_field)
        else:
            resume_value = getattr(resume, resume_field)

        # Normalize AFTER resolving the value, not based on the field name
        if isinstance(resume_value, list):
            resume_value = ", ".join(str(v) for v in resume_value)

        if isinstance(job_value, list):
            job_value = ", ".join(str(v) for v in job_value)

        score = calculate_similarity_score(str(resume_value), str(job_value))
        breakdown[job_field] = score
        total_score += score * weight

    return total_score, breakdown
