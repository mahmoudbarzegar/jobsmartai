import time

import streamlit as st

from api import call_list_jobs_api, call_score_job_api, call_cover_letter_job_api


def list_job():
    st.title("Jobs Page")
    result = call_list_jobs_api()
    data = result['result']['data']

    st.write("### Jobs")
    for i, row in enumerate(data):
        cols = st.columns([4, 1, 2, 2])
        cols[0].write(row["title"])
        if cols[1].button("View", key=i):
            st.write(f"**Details for {row['title']}:**")
            st.write(f"Resume URL: {row['resume_url']}")
            st.html(f"<strong style='font-size:25px'>Job Description:</strong><hr/>")
            st.markdown(row["description"], unsafe_allow_html=True)
            st.html("<hr/>")
        if row["score"] is None:
            if cols[2].button("Score", key=f"{row['id']}_score"):
                st.write(f"**Score for {row['title']}:**")
                with st.spinner("Loading score for this job..."):
                    time.sleep(3)  # Simulate slow data loading
                    score_result = call_score_job_api(row['id'])
                    st.html(f"<strong style='font-size:25px'>Score = {score_result['result']['score']}</strong>")
                    st.html(f"<strong style='font-size:25px'>Score Description for {row['title']}:</strong><hr/>")
                    st.write(score_result['result']['reason'])
                    st.html("<hr/>")
        else:
            if cols[2].button(f"Score = {str(row['score'])}", key=f"{row['id']}-view_score"):
                st.html(f"<strong style='font-size:25px'>Score Description for {row['title']}:</strong><hr/>")
                st.write(row["score_description"])
                st.html("<hr/>")

        if row["cover_letter"] is None:
            if cols[3].button("CL", key=f"{row['id']}_cover_letter"):
                st.write(f"**Creating a cover letter for {row['title']}:**")
                with st.spinner("Generating cover letter..."):
                    time.sleep(3)  # Simulate slow data loading
                    cover_letter_result = call_cover_letter_job_api(row['id'])
                    st.html("<hr/>")
                    st.markdown(cover_letter_result['result'], unsafe_allow_html=True)
                    st.html("<hr/>")
        else:
            if cols[3].button(f"CL View", key=f"{row['id']}-view_cover_letter"):
                st.html("<hr/>")
                st.markdown(row["cover_letter"], unsafe_allow_html=True)
                st.html("<hr/>")
