import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import streamlit as st
import seaborn as sns
import io

def create_bar_chart(df, x_columns, y_columns, stacked_bar):
    sns.set_style('dark')
    custom_colors = ['blue', 'grey', 'orange', 'red', 'green']

    # st.write(x_columns)
    x_data = df[x_columns]
    y_data = df[y_columns]
    filtered_df = pd.concat([x_data , y_data], axis = 1)
    # st.write(filtered_df)
    filtered_df.set_index(x_columns, inplace=True)
    # filtered_df.index.name = ['index']

    
    # # Convert the values to float for calculations
    filtered_df = filtered_df.astype(float)

    # st.write(filtered_df['Pd source'].unique())
    fig, ax = plt.subplots(figsize=(8, 6))
    filtered_df.plot(kind='bar', stacked=stacked_bar, ax=ax, color=custom_colors, width=0.8)  # Adjust bar width
    
    plt.xlabel(x_columns, fontsize=16)  # Set the x-axis label font size
    plt.ylabel('Total', fontsize=16)  # Set the y-axis label font size
    plt.title('Bar Chart', fontsize=20)  # Set the title font size
    plt.tight_layout()
    # Set the font size of x-axis tick labels
    plt.xticks(fontsize=12, rotation=45, ha='right')
    
    # Set the font size of y-axis tick labels
    plt.yticks(fontsize=12)
    
    # Optionally, set the legend font size
    plt.legend(fontsize=12)
    
    # Add text labels to the bars with decimal precision
    for p in ax.patches:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy() 
        ax.annotate(f'{height:.1f}', (x + width/2, y + height + 0.1), ha='center', fontsize=8)

    st.pyplot(fig)

    plot_binary = io.BytesIO()
    plt.savefig(plot_binary, format='png')
    plot_binary.seek(0)
    
    plt.close()

    return fig, plot_binary







