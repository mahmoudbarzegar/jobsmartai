import pandas as pd

from streamlit_option_menu import option_menu

from api import *

with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "Resume", "Job", "About"],
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
        result = call_create_resumes_api(files)
        if result:
            st.success("Create resumes API called successfully!")
            st.json(result)

elif selected == "Resume":
    st.title("Resume Page")
    result = call_list_resumes_api()
    data = result['result']['data']

    # Convert to DataFrame for display
    df = pd.DataFrame([{"file": d["file"]} for d in data])

    st.write("### Resumes")
    for i, row in df.iterrows():
        cols = st.columns([4, 1, 1])
        cols[0].write(row["file"])
        if cols[1].button("View", key=i):
            st.write(f"**Details for {row['file']}:**")
            st.json(data[i]["resume_info"])
        if cols[2].button("Search job"):
            result = call_search_job_api(data[i]['id'])
            st.json(result)

elif selected == "Job":
    st.title("Job Page")

    # with st.form(key="job_search_form"):
    #     keyword = st.text_input(
    #         "Enter your keyword",
    #         "python",
    #         key="placeholder",
    #     )
    #     submit_button = st.form_submit_button(label="Search")
    #
    # # Handle form submission
    # if submit_button:
    #     payload = {
    #         'keyword': keyword
    #     }
    #     result = call_search_job_api(payload)
    #     if result:
    #         st.success("Create resumes API called successfully!")
    #         st.json(result)

elif selected == "About":
    st.title("About Page")
