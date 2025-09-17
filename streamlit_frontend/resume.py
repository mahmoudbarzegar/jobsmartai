import streamlit as st

from api import call_create_resumes_api

def add_resume():
    st.title("Add a Resume")
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
        with st.spinner("Analyzing resume..."):
            result = call_create_resumes_api(files)
            if result:
                st.success("Create resumes API called successfully!")
                st.json(result)
