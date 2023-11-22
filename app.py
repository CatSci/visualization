import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# from src.saved_plots.test import create_stacked_bar_chart, create_heatmap, create_bar_plot, create_scatter_plot
from src.utils.bar_plot import create_bar_chart
from src.utils.heatmap import create_heatmap
from src.utils.scatter_plot import create_scatter_plot
from src.utils.line_plot import create_line_plot
from src.utils.grouped_stacked_bar_plot import create_stacked_bar_plot


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
</style>
"""

# Add a title to your Streamlit app with HTML markup and apply custom CSS
st.sidebar.markdown("<h1 style='text-align: center;'>CatSci</h1>" + custom_css, unsafe_allow_html=True)
# Sidebar for data upload
st.sidebar.header('Upload Data')
uploaded_file = st.sidebar.file_uploader("Choose a file")
threshold = 2
if uploaded_file is not None:
    # Read uploaded CSV data
    df = pd.read_excel(uploaded_file)
    df.replace('-', 0, inplace= True)

    # Select plot type
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Heatmap", "Scatter Plot", "Line Plot","Bar Chart", "Grouped Stacked Bar Chart"])

    # Plot based on selected options
    ##### Stacked Bar Chart plot #####

    if plot_type == 'Bar Chart':
        # df_types = pd.DataFrame(df.dtypes, columns=['Data Type'])
        # st.write(df_types.astype(str))

        x_columns = st.sidebar.multiselect('Select X-axis Column', list(df.select_dtypes(include= ['object']).columns))
        y_columns = st.sidebar.multiselect('Select Y-axis Column', list(df.select_dtypes(include=['int64', 'float64']).columns))
        stacked_bar = st.sidebar.checkbox('Stacked Bar Chart')
        if x_columns and y_columns:
            create_bar_chart(df, x_columns, y_columns, stacked_bar)
        else:
            st.warning("Please select columns to plot data")
    
    ##### Heatmap plot #####
    if plot_type == "Heatmap":
       create_heatmap(df)
    
    
    #### Scatter Plot ####
    if plot_type == "Scatter Plot":
        create_scatter_plot(df)

    if plot_type == "Line Plot":
        create_line_plot(df= df)


    if plot_type == "Grouped Stacked Bar Chart":
        grouped_column = st.sidebar.selectbox('Select column to group data', list(df.select_dtypes(include= ['object']).columns))
        x_column = st.sidebar.selectbox('Select X-axis Column', list(df.select_dtypes(include= ['object']).columns))
        y_column = st.sidebar.selectbox('Select Y-axis Column', list(df.select_dtypes(include=['int64', 'float64']).columns))
        if grouped_column and x_column and y_column:
            create_stacked_bar_plot(df, grouped_column, x_column, y_column)
        else:
            st.warning("Please select columns to plot data")


else:
    st.warning("Upload a file to get started.")

