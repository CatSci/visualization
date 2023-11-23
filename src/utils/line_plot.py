import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import io

def create_line_plot(x_axis, y_axis, df: pd.DataFrame):
    """_summary_

    Args:
        df (pd.DataFrame): _description_
    """
    
    # Select columns for X-axis and Y-axis
    fig, ax = plt.subplots(figsize=(8, 6))
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
        plt.tight_layout()
        st.pyplot(plt.gcf())

        plot_binary = io.BytesIO()
        plt.savefig(plot_binary, format='png')
        plot_binary.seek(0)
        
        plt.close()

        return fig, plot_binary
    
