import streamlit as st
from api import (
    call_ask_about_match_api,
    call_list_jobs_api,
    call_list_resumes_api,
)


def ask():
    with st.form(key="ask_form"):
        resumes = call_list_resumes_api()["result"]
        resume_options = {r["file"]: r["id"] for r in resumes}
        selected_resume_name = st.selectbox(
            "Select a resume",
            options=list(resume_options.keys()),
            key="resume_select",
        )

        jobs = call_list_jobs_api()["result"]
        job_options = {j["title"]: j["id"] for j in jobs}
        selected_job_name = st.selectbox(
            "Select a job",
            options=list(job_options.keys()),
            key="job_select",
        )

        question = st.text_input("Please enter your question: (Why is this job suitable for me?)")
        submitted = st.form_submit_button("Ask About Match")

        if question == "" and submitted:
            st.warning("Please enter your question again.")
            return

        if submitted and question:
            resume_id = resume_options[selected_resume_name]
            job_id = job_options[selected_job_name]

            with st.spinner("Processing..."):
                response = call_ask_about_match_api(resume_id=resume_id, job_id=job_id, question=question)["result"]

            st.success("Done!")
            st.write(f"**Answer:** {response['answer']}")
