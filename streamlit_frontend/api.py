import requests
import streamlit as st

API_URL = "http://localhost:8000/api"


def call_create_resumes_api(files: dict):
    url = f"{API_URL}/resumes/"
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def call_list_resumes_api():
    url = f"{API_URL}/resumes/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def call_search_job_api(resume_id: int):
    url = f"{API_URL}/jobs/search"
    try:
        payload = {"resume_id": resume_id}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def call_score_job_api(resume_id: int, job_id: int):
    url = f"{API_URL}/jobs/score"
    try:
        payload = {"resume_id": resume_id, "job_id": job_id}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None
