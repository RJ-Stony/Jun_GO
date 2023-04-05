import pandas as pd
import streamlit as st
import requests
import json

def activate_sidebar(df):
    with st.sidebar:
        uploaded_files = st.file_uploader('CSV 파일 혹은 ZIP 파일을 업로드해주세요.', accept_multiple_files=True)
    # Check if files were uploaded
    if len(uploaded_files) > 0:
        for uploaded_file in uploaded_files:
            if uploaded_file.type == 'text/csv':
                uploaded_df = pd.read_csv(uploaded_file)
                st.write(uploaded_df)

df = dict()
activate_sidebar(df)
