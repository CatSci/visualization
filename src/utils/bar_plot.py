import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import streamlit as st
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
    sns.set(font_scale = 2)
    fig, ax = plt.subplots(figsize=(15, 12))
    filtered_df.plot(kind = 'bar', stacked= stacked_bar, ax=ax, color = custom_colors)
    plt.xlabel(x_columns)
    plt.ylabel('Total')
    plt.title('Bar Chart')
    # plt.legend(bbox_to_anchor=(1, 0.5), loc='upper left')
    st.pyplot(fig)


