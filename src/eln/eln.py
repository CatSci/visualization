# from src.constant.eln_constant import API_BASE_URL
import os
# from dotenv import load_dotenv
import requests
# from flask import request
import json
import pandas as pd
import numpy as np
import streamlit as st



API_KEY = ''

API_BASE_URL = '' 


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