import streamlit as st

# Create a form
with st.form(key="resume_form"):
    uploaded_file = st.file_uploader(label="Upload your resume in PDF format", type="pdf")
    linkedin_address = st.text_input(label="Enter your LinkedIn address")
    submit_button = st.form_submit_button(label="Submit")

# Handle form submission
if submit_button:
    if uploaded_file is not None:
        st.write("Uploaded file name:", uploaded_file.name)
    else:
        st.write("No file uploaded.")
    st.write("LinkedIn address:", linkedin_address)