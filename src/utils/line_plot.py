import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def create_line_plot(df: pd.DataFrame):
    """_summary_

    Args:
        df (pd.DataFrame): _description_
    """
    
    # Select columns for X-axis and Y-axis
    x_axis_options = [col for col in df.columns]
    y_axis_options = [col for col in df.columns]
    x_axis = st.sidebar.selectbox("Select X-axis Column", x_axis_options)
    y_axis = st.sidebar.multiselect("Select Y-axis Column", y_axis_options)
    sns.set(rc={'font.size': 12}) 
    # Check if Y-axis is selected
    if y_axis:
        # Initialize chart outside the loop
        chart = None

        for y_column in y_axis:
            chart = sns.lineplot(data=df, x=x_axis, y=y_column, label=y_column, marker="o", dashes=False, errorbar= None)
        
        chart.set_xticklabels(chart.get_xticklabels(), rotation=45, horizontalalignment='right')
        chart.grid(False)
        # Move the legend outside the plot
        # plt.legend(bbox_to_anchor=(1, 0.5), loc='upper left')
        plt.title(f"Line Plot for {y_axis}")

        st.pyplot(plt.gcf())
    else:
        # Display a message if Y-axis is not selected
        st.warning("Select Y-axis to display the plot.")
