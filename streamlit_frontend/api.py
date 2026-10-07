from typing import Any

import requests
import streamlit as st

API_URL = "http://localhost:8000/api"


def call_create_resumes_api(files: dict):
    url = f"{API_URL}/resumes"
    try:
        response = requests.post(url, files=files, timeout=600)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def call_list_resumes_api():
    url = f"{API_URL}/resumes"
    try:
        response = requests.get(url, timeout=90)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def call_search_job_api(resume_id: int) -> dict | None:
    url = f"{API_URL}/jobs/search"
    try:
        payload = {"resume_id": resume_id}
        response = requests.post(url, json=payload, timeout=90)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def call_search_by_keyword_job_api(skill: str) -> dict | None:
    url = f"{API_URL}/jobs/search-by-keyword"
    try:
        payload = {"skill": skill}
        response = requests.post(url, json=payload, timeout=90)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def call_score_job_api(job_id: int):
    url = f"{API_URL}/jobs/{job_id}/score"
    try:
        response = requests.get(url, timeout=90)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def call_list_jobs_api():
    url = f"{API_URL}/jobs"
    try:
        response = requests.get(url, timeout=90)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def call_create_jobs_api(jobs_data: dict):
    url = f"{API_URL}/jobs"
    try:
        response = requests.post(url, json=jobs_data, timeout=600)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def call_cover_letter_job_api(job_id: int):
    url = f"{API_URL}/jobs/{job_id}/cover-letter"
    try:
        response = requests.get(url, timeout=90)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def call_calculate_score_application_api(application_data: dict):
    url = f"{API_URL}/applications"
    try:
        response = requests.post(url, json=application_data, timeout=300)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def call_find_best_resumes_api(job_id: int):
    url = f"{API_URL}/find-best-resumes/{job_id}"
    try:
        response = requests.get(url, timeout=90)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def call_retrieve_job_api(job_id: int):
    url = f"{API_URL}/jobs/{job_id}"
    try:
        response = requests.get(url, timeout=90)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def call_ask_about_match_api(resume_id: int, job_id: int, input_data: dict[str, Any]):
    url = f"{API_URL}/ask-about-match/job-id/{job_id}/resume-id/{resume_id}"

    st.write(f"The input_data: {input_data}")
    try:
        response = requests.post(url, json=input_data, timeout=600)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None
