import streamlit as st
import requests


def call_create_resumes_api(files: dict, data: dict):
    url = "http://localhost:8000/api/resumes/"
    try:
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


# Create a form
with st.form(key="resume_form"):
    uploaded_file = st.file_uploader(label="Upload your resume in PDF format", type="pdf")
    linkedin_address = st.text_input(label="Enter your LinkedIn address")
    submit_button = st.form_submit_button(label="Submit")

# Handle form submission
if submit_button:
    if uploaded_file is not None:
        st.write("Uploaded file name:", uploaded_file.name)
    else:
        st.write("No file uploaded.")
    st.write("LinkedIn address:", linkedin_address)

    data = {'linkedin_url': linkedin_address}
    files = {
        'file': (uploaded_file.name, uploaded_file, uploaded_file.type)
    }
    result = call_create_resumes_api(files, data)
    if result:
        st.success("Create resumes API called successfully!")
        st.json(result)
