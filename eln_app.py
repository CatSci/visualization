import streamlit as st
import pandas as pd

from src.utils.bar_plot import create_bar_chart
from src.utils.heatmap import create_heatmap, index_cols, numeric_columns
from src.utils.scatter_plot import create_scatter_plot
from src.utils.line_plot import create_line_plot
from src.utils.grouped_stacked_bar_plot import create_stacked_bar_plot

from src.eln.eln import update_plot
import requests
import json

import seaborn as sns


hide_st_Style = """
                <style>
                footer {visibility: hidden;}
                </style>
                """

st.markdown(hide_st_Style, unsafe_allow_html= True)


# Custom CSS to reduce the top margin of the app name
custom_css = """
<style>
h1 {
    margin-top: -5rem;
    font-size: 24px;
}
div.stButton > button:first-child {
    background-color: ed9439 !important
    color: white;
}
</style>
"""
# Apply HTML and CSS styling to the text input

st.markdown(
    f"""
    <style>
        div[data-baseweb="input"] input {{
            background-color: white !important;
            color: black;
            caret-color: #111b2b !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)
    # Define the button style with custom CSS
button_style = """
        display: inline-block;
            padding: 5px 20px;
            background-color: #ed9439;’
            color: #C5DFF8;
            width: 200px;
            height: 35px;
            margin-top: 20px;
            text-align: center;
            text-decoration: none;
            font-size: 16px; 
            border-radius: 8px;
"""
hover_effect = """
        color: #111b2b;
    """

st.markdown(
            f"""
            <style>
                .stButton > button {{
                    {button_style}
                }}
                .stButton:hover > button {{
                    {hover_effect}
                }}
            </style>
            """,
            unsafe_allow_html=True
        )

query_params = st.experimental_get_query_params()
eid = query_params['__eid'][0]


def upload_image_to_eln_btn(file):
    file_name = st.text_input("Enter file name")
    file_name = file_name + ".png"
    if file_name and st.button("Upload to ELN"):
        with st.spinner('Uploading plot to ELN...'):
            update_plot(eid = eid, file_name= file_name, file = plot_binary)




# Add a title to your Streamlit app with HTML markup and apply custom CSS
st.sidebar.markdown("<h1 style='text-align: center;'>CatSci</h1>" + custom_css, unsafe_allow_html=True)
# Sidebar for data upload
st.sidebar.header('Upload Data')
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    # Read uploaded CSV data

    df = pd.read_excel(uploaded_file)
    df.replace('-', 0, inplace= True)

    # Select plot type
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Heatmap", "Scatter Plot", "Line Plot","Bar Chart", "Grouped Stacked Bar Chart"])

    # Plot based on selected options

    if plot_type == 'Bar Chart':
        # df_types = pd.DataFrame(df.dtypes, columns=['Data Type'])
        # st.write(df_types.astype(str))

        x_columns = st.sidebar.multiselect('Select X-axis Column', list(df.select_dtypes(include= ['object']).columns))
        y_columns = st.sidebar.multiselect('Select Y-axis Column', list(df.select_dtypes(include=['int64', 'float64']).columns))
        stacked_bar = st.sidebar.checkbox('Stacked Bar Chart')
        if x_columns and y_columns:
            file, plot_binary = create_bar_chart(df, x_columns, y_columns, stacked_bar)
            upload_image_to_eln_btn(file= plot_binary)
            # if st.button('Upload to ELN'):
            #     with st.spinner('Uploading plot to ELN...'):
            #         pass
        else:
            st.warning("Please select columns to plot data")


    
    ##### Heatmap plot #####
    if plot_type == "Heatmap":
       st.sidebar.header("Heatmap Options")
       index_columns = index_cols(dataframe= df)
       all_numeric_columns = numeric_columns(dataframe= df)
       selected_index_rows = st.sidebar.multiselect("Select rows for Heatmap", index_columns)
       selected_time_points = st.sidebar.multiselect("Select column for Heatmap", all_numeric_columns)

       if selected_index_rows and selected_time_points:
           fig, plot_binary = create_heatmap(df = df, selected_index_rows= selected_index_rows, selected_time_points= selected_time_points)
           upload_image_to_eln_btn(file= plot_binary)
       else:
            st.warning("Please select Data")
        # if st.button('Upload to ELN'):
        #     with st.spinner('Uploading plot to ELN...'):
        #         pass
                # update_plot(plot_binary)

    #### Scatter Plot ####
    if plot_type == "Scatter Plot":
        x_axis_options = [col for col in df.columns]
        y_axis_options = [col for col in df.columns]
        x_axis = st.sidebar.selectbox("Select X-axis Column", x_axis_options)
        y_axis = st.sidebar.selectbox("Select Y-axis Column", y_axis_options)
        if x_axis and y_axis:
            fig, plot_binary = create_scatter_plot(x_axis_options=x_axis_options, x_axis= x_axis, y_axis= y_axis, df = df)
            upload_image_to_eln_btn(file= plot_binary)
        # if st.button('Upload to ELN'):
        #     with st.spinner('Uploading plot to ELN...'):
        #         pass

    if plot_type == "Line Plot":
        x_axis_options = [col for col in df.columns]
        y_axis_options = [col for col in df.columns]
        x_axis = st.sidebar.selectbox("Select X-axis Column", x_axis_options)
        y_axis = st.sidebar.multiselect("Select Y-axis Column", y_axis_options)
        if x_axis and y_axis:
            fig, plot_binary = create_line_plot(x_axis= x_axis, y_axis= y_axis, df= df)
            upload_image_to_eln_btn(file= plot_binary)
        else:
            st.warning("Select Y-axis to display the plot.")    
        # if st.button('Upload to ELN'):
        #     with st.spinner('Uploading plot to ELN...'):
        #         pass
    if plot_type == "Grouped Stacked Bar Chart":
        grouped_column = st.sidebar.selectbox('Select column to group data', list(df.select_dtypes(include= ['object']).columns))
        x_column = st.sidebar.selectbox('Select X-axis Column', list(df.select_dtypes(include= ['object']).columns))
        y_column = st.sidebar.selectbox('Select Y-axis Column', list(df.select_dtypes(include=['int64', 'float64']).columns))
        if grouped_column and x_column and y_column:
            fig = create_stacked_bar_plot(df, grouped_column, x_column, y_column)
            
        else:
            st.warning("Please select columns to plot data")
else:
    st.warning("Upload a file to get started.")

