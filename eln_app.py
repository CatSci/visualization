import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# from src.saved_plots.test import create_stacked_bar_chart, create_heatmap, create_bar_plot, create_scatter_plot
from src.utils.bar_chart import create_bar_plot
from src.utils.stacked_bar_chart import create_stacked_bar_chart
from src.utils.heatmap import create_heatmap
from src.utils.scatter_plot import create_scatter_plot


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
    # df = pd.read_excel(uploaded_file, sheet_name= 'Results  (2)')
    df = pd.read_excel(uploaded_file)
    df.replace('-', 0, inplace= True)
    # st.write(df.shape) 
    # df = df.dropna(how = 'all')
    # st.write(df)
    # st.write(df)
    # Select plot type
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Heatmap", "Scatter Plot", "Bar Plot", "Stacked Bar Chart"])

    # Plot based on selected options
    # st.header(f'{plot_type} - {x_column} vs {y_column}')
    ##### Stacked Bar Chart plot #####
    if plot_type == "Stacked Bar Chart":

        st.sidebar.header("Stacked Bar Chart Options")
        # Filter available X-axis columns based on data type (include only categorical columns)
        # x_columns = st.sidebar.multiselect(
        #     "Select X-axis Column",
        #     [col for col in df.columns if df[col].dtype == 'object' and not any(exclude in col for exclude in ["SM", "Pdt", "Im", "Unnamed"])]
        # )
        # # Populate available Y-axis columns based on plot type
        # y_columns = st.sidebar.selectbox("Select Y-axis Column", [col for col in df.columns if "SM" in col or "Pdt" in col])

        
        # to provide all column for x and y axis
        x_columns = st.sidebar.multiselect('Select X-axis Column', df.columns)
        y_columns = st.sidebar.selectbox('Select Y-axis Column', df.columns)
        hover_data = st.sidebar.selectbox('Select what data you want to display', df.columns)

        if x_columns:
            fig = create_stacked_bar_chart(df, x_columns, y_columns, hover_data)
            # Show the plot using Streamlit
            st.plotly_chart(fig)
        else:
            st.warning("Please select X axis column")
    
    ##### Heatmap plot #####
    if plot_type == "Heatmap":
       create_heatmap(df)
    

    #### Bar plot ####
    if plot_type == "Bar Plot":
        # Sidebar selection for columns
        st.sidebar.header("Bar Chart Options")
        # selected_columns = st.sidebar.multiselect("Select Columns for Y-axis", [col for col in df.columns if "SM" in col or "Pdt" in col])
        selected_columns = st.sidebar.multiselect("Select Columns for Y-axis", [col for col in df.columns])

        # Call the function with selected columns
        if selected_columns:
            create_bar_plot(df, selected_columns)
        else:
                st.warning("Please select columns to plot data")
    
    
    #### Scatter Plot ####
    if plot_type == "Scatter Plot":
        create_scatter_plot(df)


else:
    st.warning("Upload a file to get started.")

