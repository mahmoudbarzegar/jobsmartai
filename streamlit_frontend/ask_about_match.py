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

        question = st.text_area("Question", placeholder="Why is this job suitable for me?")
        top_k = st.number_input("Top K", min_value=1, max_value=20, value=5)

        st.markdown("**Resume Filters**")
        col1, col2 = st.columns(2)
        resume_skills = col1.text_input("Skills", key="resume_skills")
        resume_requirements = col2.text_input("Requirements", key="resume_requirements")
        resume_responsibilities = col1.text_input("Responsibilities", key="resume_responsibilities")
        resume_description = col2.text_input("Description", key="resume_description")

        st.markdown("**Job Filters**")
        col3, col4 = st.columns(2)
        job_skills = col3.text_input("Skills", key="job_skills")
        job_requirements = col4.text_input("Requirements", key="job_requirements")
        job_responsibilities = col3.text_input("Responsibilities", key="job_responsibilities")
        job_description = col4.text_input("Description", key="job_description")

        submitted = st.form_submit_button("Ask About Match")

        if question == "" and submitted:
            st.warning("Please enter your question again.")
            return

        if submitted and question:
            resume_id = resume_options[selected_resume_name]
            job_id = job_options[selected_job_name]

            with st.spinner("Processing..."):
                response = call_ask_about_match_api(
                    resume_id=resume_id,
                    job_id=job_id,
                    input_data={
                        "question": question,
                        "top_k": top_k,
                        "resume_filters": {
                            "skills": resume_skills,
                            "requirements": resume_requirements,
                            "responsibilities": resume_responsibilities,
                            "description": resume_description,
                        },
                        "job_filters": {
                            "skills": job_skills,
                            "requirements": job_requirements,
                            "responsibilities": job_responsibilities,
                            "description": job_description,
                        },
                    },
                )["result"]

            st.success("Done!")
            st.write(f"**Answer:** {response['answer']}")
