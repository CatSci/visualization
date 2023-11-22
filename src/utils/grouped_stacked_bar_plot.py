import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st


def create_stacked_bar_plot(dataframe, grouped_column, x_column, y_column):
    
    # colors = ["#2A66DE", "#FFC32B", "#FF5733", "#FFBD33", "#33FFBD", "#DBFF33"]
    colors = ['blue', 'grey', 'orange', 'red', 'green']

    fig = go.Figure()

    fig.update_layout(
        template="simple_white",
        xaxis=dict(title_text= str(grouped_column)),
        yaxis=dict(title_text= str(y_column)),
        barmode="stack",
        height=800,  # Set the height of the figure
        width=800,  # Set the width of the figure
        plot_bgcolor='white',  # Set the background color of the plot
        paper_bgcolor='white',  # Set the background color of the paper
        font=dict(color='black'),
    )

    for r, c in zip(dataframe[grouped_column].unique(), colors):
        plot_df = dataframe[dataframe[grouped_column] == r]
        
        text_values = plot_df[y_column].tolist()  # Get the y values for text labels
        
        fig.add_trace(
            go.Bar(
                x=[plot_df[grouped_column], plot_df[x_column]],
                y=plot_df[y_column],
                text=text_values,
                name=r,
                marker_color=c,
                textposition='inside',  # Adjust the position of text labels
            ),
        )
    
    st.plotly_chart(fig)


