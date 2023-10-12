import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns

def create_bar_chart(df, x_columns, y_columns, stacked_bar):
    sns.set_style('dark')
    custom_colors = ['blue', 'grey', 'orange', 'red', 'green']

    # st.write(x_columns)
    x_data = df[x_columns]
    y_data = df[y_columns]
    filtered_df = pd.concat([x_data , y_data], axis = 1)
    filtered_df.set_index(x_columns, inplace=True)

    # Convert the values to float for calculations
    filtered_df = filtered_df.astype(float)

    # Create the 100% stacked bar chart using Seaborn
    fig, ax = plt.subplots(figsize=(12, 10))
    filtered_df.plot(kind = 'bar', stacked= stacked_bar, ax=ax, color = custom_colors)
    plt.xlabel(x_columns)
    plt.ylabel('Total')
    plt.title('Bar Chart')
    st.pyplot(fig)


