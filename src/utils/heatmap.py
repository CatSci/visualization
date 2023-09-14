import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from src.utils.utils import generate_colors

def create_heatmap(df):
    st.info('Please select Experiment # column first', icon="ℹ️")
    st.sidebar.header("Heatmap Options")
    
    # time_points = [col for col in df.columns if "Pdt" in col or "SM" in col]

    df = df.astype(str)

    # selected_index_rows = st.sidebar.multiselect("Select rows for Heatmap", 
    #                                              [col for col in df.columns if df[col].dtype == 'object' and not any(exclude in col for exclude in ["SM", "Pdt", "Im", "Unnamed"])])

    # # Select time points to display in the heatmap
    # selected_time_points = st.sidebar.multiselect("Select Time Points", time_points)

    # to provide all column for x and y axis
    selected_index_rows = st.sidebar.multiselect("Select rows for Heatmap", 
                                                 [col for col in df.columns])
    selected_time_points = st.sidebar.multiselect("Select Time Point", [col for col in df.columns])
    

    if selected_time_points:
        # Specify the desired order of experiments
        experiment_order = df['Exp #'].unique()  # Replace with the desired order
        

        heatmap_data = pd.pivot_table(df,
            index=selected_index_rows, 
            values=selected_time_points, 
            aggfunc= 'first',
            fill_value=0  # Fill missing values with 0 or another appropriate value
        )
        # st.write(heatmap_data)
        
        if not selected_index_rows:
            # If no rows are selected, keep the original order (no reindexing)
            heatmap_data = heatmap_data[experiment_order]
        else:
            # Reorder the experiments if rows are selected
            heatmap_data = heatmap_data.reindex(experiment_order, level=0)

        if not heatmap_data.empty:
            heatmap_data = heatmap_data.reindex(columns=selected_time_points)  # Reorder the columns
            heatmap_data = heatmap_data.astype(float)
            # Create a Seaborn heatmap with custom aesthetics
            plt.figure(figsize=(18, 15))
            sns.set(font_scale=2)  # Adjust font size
            
            # Customize the color bar appearance to add some gap
            cbar_kws = {
                'orientation': 'vertical',
                'pad': 0.03,  # Adjust the padding between the heatmap and color bar
                'shrink': 0.8  # Reduce the size of the color bar to add a gap
            }

            sns.heatmap(data=heatmap_data, cmap='YlOrBr', annot=True, fmt=".2f", cbar=True,
                        linewidths=0.5, linecolor='black', cbar_kws=cbar_kws)
            plt.xlabel('Time Points')
            plt.ylabel(selected_index_rows)
            plt.title(f'Concentrations with different {selected_index_rows} ')

            # Display the heatmap using Streamlit by passing the Matplotlib figure
            st.pyplot(plt.gcf())  # Pass the current figure (gcf)
        else:
            st.warning("No data available for the selected options")
    else:
        st.warning("Please select Time Points")