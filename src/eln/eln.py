# from src.constant.eln_constant import API_BASE_URL
import os
# from dotenv import load_dotenv
import requests
# from flask import request
import json
import pandas as pd
import numpy as np
import streamlit as st

from dotenv import load_dotenv

# load_dotenv(".env")
# API_KEY = os.getenv("API_KEY")
# API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = st.secrets["API_KEY"]
API_BASE_URL = st.secrets["API_BASE_URL"]

def update_plot(eid, file, file_name):
    # Prepare the files parameter for the POST request
    # files = {'file': (file_name, file, 'image/png')}
    # Define headers
    headers = {
        'accept': 'application/vnd.api+json',
        'Content-Type': 'application/octet-stream',
        'x-api-key': API_KEY
    }

    try:
        API_URL = API_BASE_URL + eid + "/children/" + file_name + "?force=true"

        response = requests.post(API_URL, headers=headers, data= file)

        if response.status_code == 201:
            st.success("Image is uploaded")
        else:
            st.error(f"Error {response.status_code}")
    except Exception as e:
        print(f"Error: {str(e)}")


