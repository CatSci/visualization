import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from src.utils.utils import generate_colors
import io 
from src.eln.eln import update_plot, update_plot_plotly



def index_cols(dataframe: pd.DataFrame) -> list:
    """
    Args:
        df (_type_): _description_
    """
    # Get all columns with object data type
    object_columns = list(dataframe.select_dtypes(include=['object']).columns)

    # Filter out columns containing "SM," "Pdt," or "Im"
    index_columns = [
        col for col in object_columns 
        if not any(keyword in col for keyword in ["SM", "Pdt", "Im"])
    ]
    return index_columns



def numeric_columns(dataframe: pd.DataFrame) -> list:
    """_summary_

    Args:
        dataframe (pd.DataFrame): _description_

    Returns:
        list: _description_
    """
    # Get the numeric columns
    numeric_columns = list(dataframe.select_dtypes(include=['int64', 'float64']).columns)
    # Get the columns containing "SM," "Pdt," or "Im" without duplicates and in the order of appearance
    numeric_obj_columns = []
    for col in dataframe.columns:
        if (
            any(keyword in col for keyword in ["SM", "Pdt", "Im"]) 
            and col not in numeric_obj_columns 
            and col not in numeric_columns
        ):
            numeric_obj_columns.append(col)
    # Combine numeric and additional columns while removing duplicates
    all_numeric_columns = numeric_columns + numeric_obj_columns
    
    return all_numeric_columns




def create_heatmap(df):
    # st.info('Please select Experiment # column first', icon="ℹ️")
    st.sidebar.header("Heatmap Options") 

    index_columns = index_cols(dataframe= df)
    all_numeric_columns = numeric_columns(dataframe= df)

    # to provide all column for x and y axis
    selected_index_rows = st.sidebar.multiselect("Select rows for Heatmap", index_columns)
    selected_time_points = st.sidebar.multiselect("Select column for Heatmap", all_numeric_columns)

    # add uid column to dataframe which will be unique
    if any(col in df.columns for col in ["Exp #", "Exp"]):
        if "Exp #" in df.columns and len(df["Exp #"].unique()) != len(df):
            df["uid"] = range(1, len(df) + 1)
            selected_index_rows.insert(0, 'uid')
        elif "Exp" in df.columns and len(df["Exp"].unique()) != len(df):
            df["uid"] = range(1, len(df) + 1)
            selected_index_rows.insert(0, 'uid')
        else:
            if "Exp #" in df.columns:
                selected_index_rows.insert(0, 'Exp #')
            elif "Exp" in df.columns:
                selected_index_rows.insert(0, 'Exp')
    else:
        df["uid"] = range(1, len(df) + 1)
        selected_index_rows.insert(0, 'uid')


    order = selected_index_rows[0]
    if selected_time_points:
        # Specify the desired order of experiments
        experiment_order = df[order]  # Replace with the desired order

        heatmap_data = pd.pivot_table(df,
            index=selected_index_rows, 
            values=selected_time_points, 
            aggfunc= 'first',
            fill_value=0  # Fill missing values with 0 or another appropriate value
        )

        
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
            sns.set(font_scale=2.5)  # Adjust font size
            
            # Customize the color bar appearance to add some gap
            cbar_kws = {
                'orientation': 'vertical',
                'pad': 0.03,  # Adjust the padding between the heatmap and color bar
                'shrink': 0.8  # Reduce the size of the color bar to add a gap
            }

            sns.heatmap(data=heatmap_data, cmap='YlOrBr', annot=True, fmt=".2f", cbar=True,
                        linewidths=0.5, linecolor='black', cbar_kws=cbar_kws)
            plt.ylabel(selected_index_rows)
            plt.title(f'Output with different {selected_index_rows} ', pad= 30)
            # Adjust x-axis ticks and label position
            plt.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False, labeltop=True)

            # Display the heatmap using Streamlit by passing the Matplotlib figure
            st.pyplot(plt.gcf())  # Pass the current figure (gcf)

            # Instead of displaying the plot, save it as a binary image
            plot_binary = io.BytesIO()
            plt.savefig(plot_binary, format='png')
            plot_binary.seek(0)  # Move the stream pointer to the beginning
            # Close the plot to release resources
            plt.close()
            
            

            return plot_binary
        else:
            st.warning("No data available for the selected options")
    else:
        st.warning("Please select Time Points")