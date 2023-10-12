import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from src.utils.utils import generate_colors
import io, tempfile, base64



def create_bar_plot(df, selected_columns):
    # Define a custom colormap
    custom_colormap = ['viridis']
    colormap = 'Plasma'

    # Filter the DataFrame based on selected columns
    selected_df = df[['Exp #'] + selected_columns]

    # Create a trace for each selected column
    traces = []
    # Generate a list of colors for the bars
    num_colors = len(selected_columns)
    colors = generate_colors(num_colors)

    for i, column in enumerate(selected_columns):
        trace = go.Bar(
            x=selected_df['Exp #'],
            y=selected_df[column],
            name=column,
            text=selected_df[column],
            textposition='outside',
            width=0.2,
            marker_color=colors[i],
            texttemplate='%{text}',  # Format the text label
            textfont=dict(size=16),  # Customize the text font size
        )
        # trace.marker.color = custom_colormap
        traces.append(trace)

    # Create the bar chart using Plotly
    fig = go.Figure(traces)

    # Customize the layout
    fig.update_layout(
        barmode='group',  # 'group' for grouped bars, 'stack' for stacked bars
        title='Concentration for Each Experiment',
        xaxis_title='Experiment',
        yaxis_title='Concentration',
        showlegend=True,
        width=1000,
        height=600,
        plot_bgcolor="rgba(255, 255, 255, 255)",
        bargap=0.3,
        xaxis_showgrid=False,  # Remove x-axis grid lines
        yaxis_showgrid=False,
        xaxis=dict(
            tickmode='array',  # Use specified tick values
            tickvals=selected_df['Exp #'],  # Set tick values to experiment numbers
            dtick=1,  # Set tick interval to 1
        )
    )

    # Display the bar chart using Streamlit
    st.plotly_chart(fig)