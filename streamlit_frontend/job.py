import time
from typing import Any

import streamlit as st
from api import (
    call_calculate_score_application_api,
    call_create_jobs_api,
    call_find_best_resumes_api,
    call_list_jobs_api,
    call_list_resumes_api,
    call_retrieve_job_api,
    call_search_by_keyword_job_api,
)


def list_job():
    st.title("Jobs Page")
    result = call_list_jobs_api()
    jobs = result["result"]

    st.write("### Jobs")
    for _, job in enumerate(jobs):
        st.session_state[f"show_form_{job['id']}"] = False

        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

        col1.write(job["title"])

        if col2.button("View", key=f"view_{job['id']}"):
            del st.session_state[f"show_form_{job['id']}"]
            st.write(f"**Details for {job['title']}:**")
            st.html("<strong style='font-size:25px'>Job Description:</strong><hr/>")
            st.markdown(job["description"], unsafe_allow_html=True)
            st.html("<hr/>")

        if col3.button("History", key=f"history_{job['id']}"):
            del st.session_state[f"show_form_{job['id']}"]
            for _, application in enumerate(job["job_applications"]):
                st.html(f"<strong style='font-size:18px'>Resume_link: </strong>{application['resume_link']}")
                st.html(f"<strong style='font-size:18px'>Score: </strong> {round(application['score'] * 100, 1)}")
                st.html("<strong style='font-size:18px'>Score Description:</strong>")
                st.markdown(application["score_description"], unsafe_allow_html=True)
                st.html("<hr/><hr/>")

        if col4.button("Apply", key=f"apply_{job['id']}"):
            st.session_state[f"show_form_{job['id']}"] = True

        if st.session_state.get(f"show_form_{job['id']}"):
            with st.form(key=f"apply_form_{job['id']}"):
                resumes = call_list_resumes_api()["result"]
                resume_options = {r["file"]: r["id"] for r in resumes}

                selected_resume_name = st.selectbox(
                    "Select a resume",
                    options=list(resume_options.keys()),
                    key=f"resume_select_{job['id']}",
                )

                submitted = st.form_submit_button("Submit")

                if submitted:
                    resume_id = resume_options[selected_resume_name]

                    with st.spinner("Processing..."):
                        response = call_calculate_score_application_api({"resume_id": resume_id, "job_id": job["id"]})[
                            "result"
                        ]

                    st.success("Done!")
                    st.write(f"**Match score:** {round(response['score'] * 100, 1)}")
                    st.write(f"**Score Description:** {response['score_description']}")
                    st.write(f"**Status:** {response['status']}")

        if col5.button("Find Related Resumes", key=f"resume_related_{job['id']}"):
            del st.session_state[f"show_form_{job['id']}"]
            with st.spinner("Finding related resumes..."):
                time.sleep(3)  # Simulate slow data loading
                find_best_resumes_result = call_find_best_resumes_api(job["id"])
                if find_best_resumes_result["status"] == "success":
                    job_result = call_retrieve_job_api(job["id"])
                    for _, application in enumerate(job_result["job_applications"]):
                        st.html(f"<strong style='font-size:18px'>Resume_link: </strong>{application['resume_link']}")
                        st.html(
                            f"<strong style='font-size:18px'>Score: </strong> {round(application['score'] * 100, 1)}"
                        )
                        st.html("<strong style='font-size:18px'>Score Description:</strong>")
                        st.markdown(application["score_description"], unsafe_allow_html=True)
                        st.html("<hr/><hr/>")


def add_job():
    with st.form(key="job_form"):
        title = st.text_input("Enter job title:")
        link = st.text_input("Enter job link:")
        description = st.text_area("Enter job description:", height=375)
        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            with st.spinner("Storing job"):
                result = call_create_jobs_api({"title": title, "description": description, "link": link})
                if result:
                    st.success("Create Jobs API called successfully!")
                    st.json(result)


def search_job():
    st.title("Search jobs by keyword")
    with st.form(key="search_job_form"):
        keyword = st.text_input("Enter a job keyword")
        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            if keyword.strip() == "" or keyword is None:
                st.write("Please enter a skill keyword.")
                return

            st.write("Skill Keyword:", keyword)
            with st.spinner("Search jobs..."):
                result: Any = call_search_by_keyword_job_api(skill=keyword)
                jobs = result["result"]["jobs"]
                for _, item in enumerate(jobs):
                    cols = st.columns([2, 5])
                    cols[0].write(item["title"])
                    cols[1].write(item["link"])
