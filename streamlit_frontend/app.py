import time

import pandas as pd
from streamlit_option_menu import option_menu

from api import *

with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "Resume", "About"],
        icons=["house", "file-earmark", "briefcase", "info-circle"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    st.title("Home Page")
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

elif selected == "Resume":
    st.title("Resume Page")
    result = call_list_resumes_api()
    data = result['result']['data']

    # Initialize session_state dicts for tracking button clicks if not present
    if "view_clicked" not in st.session_state:
        st.session_state.view_clicked = {}

    if "search_job_clicked" not in st.session_state:
        st.session_state.search_job_clicked = {}

    if "score_clicked" not in st.session_state:
        st.session_state.score_clicked = {}

    st.write("### Resumes")
    for i, row in enumerate(data):
        cols = st.columns([4, 1, 1])
        cols[0].write(data[i]["file"])

        # View button
        if cols[1].button("View", key=f"view_{row['id']}"):
            st.session_state.view_clicked[row['id']] = True
        if st.session_state.view_clicked.get(row['id'], False):
            st.write(f"**Details for {row['file']}:**")
            st.json(row["resume_info"])

        # Search job button
        if cols[2].button("Search job", key=f"search_{row['id']}"):
            st.session_state.search_job_clicked[row['id']] = True

        if st.session_state.search_job_clicked.get(row['id'], False):
            st.session_state.view_clicked[row['id']] = True
            st.write("### Jobs")
            with st.spinner("Loading jobs..."):
                time.sleep(3)  # Simulate slow data loading
                result = call_search_job_api(row['id'])
                jobs = result['result']['jobs']
                for index, item in enumerate(jobs):
                    job_cols = st.columns([2, 5, 1])
                    job_cols[0].write(item["title"])
                    job_cols[1].write(item["link"])
                    if job_cols[2].button("Score", key=f"score_{row['id']}_{item['id']}"):
                        st.write("### Get Job Score")
                        st.session_state.score_clicked[(row['id'], item['id'])] = True
                    if st.session_state.score_clicked.get((row['id'], item['id']), False):
                        with st.spinner("Loading score..."):
                            time.sleep(3)  # Simulate slow data loading
                            job_score_result = call_score_job_api(resume_id=row['id'], job_id=item['id'])
                            st.write(job_score_result['result'])

elif selected == "About":
    st.title("About Page")
