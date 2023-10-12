import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from src.utils.utils import generate_colors
import io, base64
import plotly.io as pio
import requests
import plotly.offline as pyo



def create_stacked_bar_chart(df, x_columns, y_columns, hover_data):
    """_summary_

    Args:
        df (_type_): _description_
        x_columns (_type_): _description_
        y_columns (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Create a trace for each experiment
    traces = []

    for i, exp_num in enumerate(df['Exp #'].unique()):
        exp_df = df[df['Exp #'] == exp_num]
        x_labels = exp_df.apply(lambda row: ' - '.join(str(row[x]) for x in x_columns), axis=1).tolist()
        trace = go.Bar(
            x=x_labels,
            y=exp_df[y_columns],
            name=f'Experiment {exp_num}',
            text=exp_df[y_columns],
            textposition='auto',
        )
        traces.append(trace)

    fig = go.Figure(data=traces)

    fig.update_layout(
        title='Stacked Bar Chart for',
        xaxis_title='Reaction Conditions',
        yaxis_title= y_columns,
        barmode='stack',  # Use 'stack' for a stacked bar chart
        legend_title_text='Experiments',
        plot_bgcolor="rgba(255, 255, 255, 255)",
        showlegend=True,
        width=1000,
        height=600,
        xaxis_showgrid=False,  # Remove x-axis grid lines
        yaxis_showgrid=False,  # Remove y-axis grid lines
    )

    return fig





# def upload_png_to_api(png_filename, API_BASE_URL, API_KEY):
#     try:
#             # Convert the Plotly figure to an image in bytes format
#             img_bytes = pio.to_image(fig, format="png")

#             # Create a file-like object from the bytes data
#             img_file = io.BytesIO(img_bytes)

#             # Create a dictionary containing the file (image) to be uploaded
#             files = {'file': ('chart.png', img_file)}


#             headers = {
#                 'accept': 'application/vnd.api+json',
#                 'Content-Type': 'application/octet-stream',
#                 'x-api-key': API_KEY
#             }

#             # In the request body, include the PNG file data
#             response = requests.post(API_BASE_URL, headers=headers, files=files)

#             if response.status_code == 201:
#                 st.write("PNG image uploaded successfully.")
#                 return response.json()  # You can return the API's response if it provides any
#             else:
#                 st.write(f"Failed to upload PNG image. Status code: {response.status_code}")
#                 return None
#     except Exception as e:
#         st.write(f"Error uploading PNG image: {str(e)}")
#         return None

# def create_stacked_bar_chart(df, x_columns, y_columns, hover_data):
#     """Create a stacked bar chart using Seaborn.

#     Args:
#         df (pd.DataFrame): The DataFrame containing the data.
#         x_columns (list): List of column names for the x-axis.
#         y_columns (list): List of column names for the y-axis.

#     Returns:
#         plt.figure: The Seaborn figure object.
#     """
    
    # Filter the DataFrame based on selected X-columns
    # filtered_df = df[x_columns + [y_columns, 'Exp #']]
    # st.write(filtered_df)
    # # Pivot the DataFrame for creating a stacked bar chart
    # pivoted_df = filtered_df.pivot(index= 'Exp #', columns= x_columns, values=y_columns)

    # # Reset the index to remove X-columns from the index
    # pivoted_df = pivoted_df.reset_index()

    # # Create the stacked bar chart using Seaborn
    # plt.figure(figsize=(10, 6))
    # sns.barplot(
    #     data=pivoted_df,
    #     ci=None,  # Disable confidence intervals if not needed
    # )

    
    # # Customize the plot
    # plt.title('Stacked Bar Chart')
    # plt.xlabel(', '.join(x_columns))
    # plt.ylabel(y_columns)
    # plt.legend(title="Experiments", labels=[f'Experiment {exp_num}' for exp_num in df['Exp #'].unique()])
    # plt.grid(axis="y", linestyle="--", alpha=0.7)

    # filtered_df = df[x_columns + [y_columns, hover_data, 'Exp #']]
    # st.write(filtered_df)

    # # Pivot the DataFrame for creating a stacked bar chart
    # pivoted_df = filtered_df.pivot(index=x_columns, columns='Exp #', values=y_columns)

    # # Reset the index to remove X-columns from the index
    # pivoted_df = pivoted_df.reset_index()

    # # Create the stacked bar chart using Seaborn
    # plt.figure(figsize=(10, 6))
    # sns.barplot(
    #     data=pivoted_df,
    #     errorbar=None,  # Disable confidence intervals if not needed,
    #     palette='viridis',
    # )

    # # Customize the plot
    # plt.title('Stacked Bar Chart')
    # plt.xlabel(', '.join(x_columns))
    # plt.ylabel(y_columns)
    # plt.legend(title="Experiments", labels=[f'Experiment {exp_num}' for exp_num in df['Exp #'].unique()])
    # plt.grid(axis="y", linestyle="--", alpha=0.7)
    # st.pyplot(plt.gcf())
    # return plt

# Upload the stacked bar chart to CatSci using the API
# def upload_stacked_bar_chart(fig):
#     """Uploads a stacked bar chart to CatSci using the API.

#     Args:
#         fig: A Plotly figure object.

#     Returns:
#         The URL of the uploaded image.
#     """

#     # Convert the stacked bar chart to a PNG image
#     image_data = io.BytesIO()
#     pio.write_image(fig, image_data, format="png")

#     image_data.seek(0)

#     # Create a new POST request to the API endpoint

#     headers = {
#         'accept': 'application/vnd.api+json',
#         'Content-Type': 'application/octet-stream',
#         'x-api-key': API_KEY
#     }

#     # In the request body, include the PNG image data
#     response = requests.post(API_BASE_URL, headers=headers, data=image_data.getvalue())

#     # Check if the request was successful
#     if response.status_code == 201:
#         # The image was successfully uploaded
#         image_url = response.json()["url"]

#         return image_url
#     else:
#         # An error occurred while uploading the image
#         raise Exception("An error occurred while uploading the image.")