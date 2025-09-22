from streamlit_multi_menu import streamlit_multi_menu

from api import *
from resume import add_resume, list_resume
from job import list_job

sub_menus = {
    "Resume": ["Add Resume", "List Resume"],
    "Job": ["Add Job", "List Job", "Search Job"],
}

sub_menu_icons = {
    "Resume": ["add", "list"],
    "Job": ["add", "list", "search"],
}
selected_menu = streamlit_multi_menu(
    menu_titles=list(sub_menus.keys()),
    sub_menus=sub_menus,
    sub_menu_icons=sub_menu_icons,
    use_container_width=True
)

if selected_menu == "Add Resume" or selected_menu is None:
    add_resume()
elif selected_menu == "List Resume":
    list_resume()
elif selected_menu == "List Job":
    list_job()
elif selected_menu == "Add Job":
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

elif selected_menu == "About":
    st.title("About Page")
