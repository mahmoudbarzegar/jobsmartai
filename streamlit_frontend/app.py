import time

from streamlit_option_menu import option_menu

from api import *

with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "Resumes", "Jobs", "Rapid", "About"],
        icons=["house", "file-earmark", "briefcase", "speedometer", "info-circle"],
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

elif selected == "Resumes":
    st.title("Resumes Page")
    result = call_list_resumes_api()
    data = result['result']['data']

    st.write("### Resumes")
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

elif selected == "Jobs":
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

elif selected == "Rapid":
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

elif selected == "About":
    st.title("About Page")
