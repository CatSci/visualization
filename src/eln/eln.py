# from src.constant.eln_constant import API_BASE_URL
import os
# from dotenv import load_dotenv
import requests
# from flask import request
import json
import pandas as pd
import numpy as np
import streamlit as st
from IPython.display import Image


# API_BASE_URL = 'https://catsci.signalsnotebook.perkinelmercloud.eu/api/rest/v1.0/adt/'
API_KEY = 'NvPkEXLMW96UwVjsF+dDAjs8CROAtlXFG9dc9o38HTTZ/6dTIrV1sWELAa0vRvVqHHawTg=='

API_BASE_URL = 'https://catsci-sandbox.signalsnotebook.perkinelmercloud.eu/api/rest/v1.0/entities/experiment%3Abe685e48-2593-4e74-8ad4-9d8b2dc36514/children/a.png?force=true' \


def update_plot(path):
    # Define headers
    headers = {
        'accept': 'application/vnd.api+json',
        'Content-Type': 'application/octet-stream',
        'x-api-key': API_KEY
    }

    try:

        # with open(path, 'rb') as file:
        response = requests.post(API_BASE_URL, headers=headers, data= path)

        if response.status_code == 201:
            print("Success: The POST request was successful.")
        else:
            print(f"Error: The POST request returned status code {response.status_code}")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_plot_plotly(file_path):
    # Define headers
    headers = {
        'accept': 'application/vnd.api+json',
        'x-api-key': API_KEY
    }

    #  # Read the file's content
    # with open(file_path, 'rb') as image_file:
    #     file_content = image_file.read()

    # Create a POST request to upload the image with the file's content
    files = {'image': ('image.png', file_path, 'image/png')}
    response = requests.post(API_BASE_URL, headers=headers, files=files)

    # Check if the upload was successful
    if response.status_code == 201:
        return True
    else:
        return False