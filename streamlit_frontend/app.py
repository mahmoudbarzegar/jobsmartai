import streamlit as st
import pandas as pd

st.file_uploader(label="Upload your resume in PDF format", type="pdf")
st.text_input(label="Enter your linkedin address",icon=":material/link:")
st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))
