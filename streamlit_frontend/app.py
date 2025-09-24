from streamlit_multi_menu import streamlit_multi_menu

from api import *
from resume import add_resume, list_resume
from job import list_job, add_job

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
    add_job()
elif selected_menu == "About":
    st.title("About Page")
