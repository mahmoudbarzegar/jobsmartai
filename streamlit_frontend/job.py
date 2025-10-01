import time

from api import *


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


def add_job():
    result = call_list_resumes_api()
    data = result['result']['data']
    options_list = [row["file"] for row in data]
    with st.form(key="job_form"):
        selected_option = st.selectbox("Select an item", options_list)
        selected_id = next(row["id"] for row in data if row["file"] == selected_option)
        title = st.text_input("Enter job title:")
        description = st.text_area("Enter job description:")
        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            with st.spinner("Store job and get score..."):
                result = call_create_jobs_api({
                    'resume_id': selected_id,
                    'title': title,
                    'description': description,

                })
                if result:
                    st.success("Create Jobs API called successfully!")
                    st.json(result)


def search_job():
    st.title("Search jobs by keyword")
    with st.form(key="search_job_form"):
        keyword = st.text_input("Enter a job keyword")
        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            if keyword is not None:
                st.write("Skill Keyword:", keyword)
            else:
                st.write("Please enter a skill keyword.")

            with st.spinner("Search jobs..."):
                result = call_search_by_keyword_job_api(skill=keyword)
                jobs = result['result']['jobs']
                for index, item in enumerate(jobs):
                    cols = st.columns([2, 5])
                    cols[0].write(item["title"])
                    cols[1].write(item["link"])

