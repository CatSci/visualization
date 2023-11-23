import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import io



def create_scatter_plot(x_axis_options, x_axis, y_axis, df: pd.DataFrame):
    """_summary_

    Args:
        df (pd.DataFrame): _description_
    """
    
    # Select columns for X-axis and Y-axis
    
    # x_axis = st.sidebar.selectbox("Select X-axis Column", x_axis_options)
    # y_axis = st.sidebar.selectbox("Select Y-axis Column", y_axis_options)

    # Select columns for hue, size, etc.
    # Exclude the selected x_axis from hue and size options
    available_columns = [col for col in x_axis_options if col not in x_axis]
    hue_column = st.sidebar.selectbox("Select Hue Column", available_columns)
    # Create a list of size options, including "None"
    numeric_columns = [col for col in available_columns if df[col].dtype in ['int64', 'float64']]
    
    size_options = ['None'] + numeric_columns
    size_column = st.sidebar.selectbox("Select Size Column", size_options)
    
    if size_column == 'None':
        size_column = None
    sns.set(font_scale=1.5)
    fig, ax = plt.subplots(figsize=(12, 10))
    chart = sns.scatterplot(data= df, x= x_axis, y= y_axis, hue= hue_column, size= size_column, sizes=(100, 300))
    chart.set_xticklabels(chart.get_xticklabels(), rotation=45, horizontalalignment='right')
    # chart.grid(False)
    plt.legend(bbox_to_anchor=(1, 0.7), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt.gcf())

    plot_binary = io.BytesIO()
    plt.savefig(plot_binary, format='png')
    plot_binary.seek(0)
    
    plt.close()

    return fig, plot_binary
