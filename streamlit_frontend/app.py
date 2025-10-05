import streamlit as st

from streamlit_option_menu import option_menu

from resume import add_resume, list_resume
from job import list_job, add_job, search_job

styles = {
    "container": {"background-color": "#FFFFFF"},
    "menu-title": {"color": "#285E82", "font-size": "25px", "font-weight": "bold"},
    "icon": {"color": "#285E82"},
    "nav": {"color": "#333333", "font-size": "18px"},
    "nav-link": {"color": "#333333"},
    "nav-link-selected": {"background-color": "#3A7CA5", "color": "white"},
    "hover": {"background-color": "#ddd", "color": "#000000"},
}



with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Add Resume", "List Resume", "Add Job", "List Job", "Search Job"],
        icons=["file-earmark-person", "list-columns-reverse", "plus-square", "list-columns-reverse", "search"],
        menu_icon="cast",
        default_index=0,
        styles=styles
    )

if selected == "Add Resume" or selected is None:
    add_resume()
elif selected == "List Resume":
    list_resume()
elif selected == "List Job":
    list_job()
elif selected == "Add Job":
    add_job()
elif selected == "Search Job":
    search_job()
