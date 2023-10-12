import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import plotly.io as pio
from src.utils.utils import generate_colors



def create_scatter_plot(df: pd.DataFrame):
    """_summary_

    Args:
        df (pd.DataFrame): _description_
    """
    
    # Select columns for X-axis and Y-axis
    x_axis_options = [col for col in df.columns]
    y_axis_options = [col for col in df.columns]
    x_axis = st.sidebar.selectbox("Select X-axis Column", x_axis_options)
    y_axis = st.sidebar.selectbox("Select Y-axis Column", y_axis_options)

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

    # Create scatter plot
    fig = px.scatter(
        df,
        x=x_axis,
        y=y_axis,
        color=hue_column,
        size=size_column,
        title=f"Scatter Plot: {x_axis} vs {y_axis}",
    )

    fig.update_layout(
        xaxis_title=x_axis,
        yaxis_title=y_axis,
        showlegend=True,
        legend_title=hue_column,
        legend=dict(
            x=1.02,  # Adjust the legend position
        ),
        margin=dict(l=0, r=50, b=50, t=50),  # Adjust the margins as needed
        width=800,
        height=600,
        xaxis_showgrid=False,  # Remove x-axis grid lines
        yaxis_showgrid=False,
        plot_bgcolor="rgba(0, 0, 0, 0)",
    )

    # # Show the plot
    st.plotly_chart(fig)
