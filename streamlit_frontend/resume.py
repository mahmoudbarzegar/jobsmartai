import time

import streamlit as st

from api import call_create_resumes_api, call_list_resumes_api, call_search_job_api


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


def list_resume():
    st.title("List Resumes")
    result = call_list_resumes_api()
    data = result['result']['data']

    for i, row in enumerate(data):
        cols = st.columns([4, 1, 1])
        cols[0].write(row["file"])
        if cols[1].button("View", key=i):
            st.write(f"**Details for {row['file']}:**")
            st.json(row["resume_info"])
        if cols[2].button("Search job", key=f"{row['id']}_search_job"):
            st.write("### Jobs")
            with st.spinner("Loading jobs..."):
                time.sleep(3)  # Simulate slow data loading
                result = call_search_job_api(row['id'])
                jobs = result['result']['jobs']
                for index, item in enumerate(jobs):
                    cols = st.columns([2, 5])
                    cols[0].write(item["title"])
                    cols[1].write(item["link"])
