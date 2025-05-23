import streamlit as st
import requests


def call_create_resumes_api(files: dict):
    url = "http://localhost:8000/api/resumes/"
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


# Create a form
with st.form(key="resume_form"):
    uploaded_file = st.file_uploader(label="Upload your resume in PDF format", type="pdf")
    submit_button = st.form_submit_button(label="Submit")

# Handle form submission
if submit_button:
    if uploaded_file is not None:
        st.write("Uploaded file name:", uploaded_file.name)
    else:
        st.write("No file uploaded.")

    files = {
        'file': (uploaded_file.name, uploaded_file, uploaded_file.type)
    }
    result = call_create_resumes_api(files)
    if result:
        st.success("Create resumes API called successfully!")
        st.json(result)
