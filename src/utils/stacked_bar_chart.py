import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from src.utils.utils import generate_colors


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