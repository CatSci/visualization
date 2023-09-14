import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def create_stacked_bar_chart(df, x_columns, y_columns):
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
        title='Stacked Bar Chart for ' + y_columns,
        xaxis_title='Reaction Conditions',
        yaxis_title= y_columns,
        barmode='stack',  # Use 'stack' for a stacked bar chart
        legend_title_text='Experiments',
        plot_bgcolor="rgba(0, 0, 0, 0)",
        showlegend=True,
        width=1000,
        height=600,
        xaxis_showgrid=False,  # Remove x-axis grid lines
        yaxis_showgrid=False,  # Remove y-axis grid lines
    )

    return fig



def create_heatmap(df):
    st.info('Please select Experiment # column first', icon="ℹ️")
    st.sidebar.header("Heatmap Options")
    
    time_points = [col for col in df.columns if "Pdt" in col or "SM" in col]

    df = df.astype(str)

    selected_index_rows = st.sidebar.multiselect("Select rows for Heatmap", 
                                                 [col for col in df.columns if df[col].dtype == 'object' and not any(exclude in col for exclude in ["SM", "Pdt", "Im", "Unnamed"])])

    # Select time points to display in the heatmap
    selected_time_points = st.sidebar.multiselect("Select Time Points", time_points)


    if selected_time_points:
        # Specify the desired order of experiments
        experiment_order = df['Exp #'].unique()  # Replace with the desired order
        

        heatmap_data = df.pivot_table(
            index=selected_index_rows, 
            values=selected_time_points, 
            fill_value=0  # Fill missing values with 0 or another appropriate value
        ).reindex(experiment_order, level=0)  # Reorder the experiments
        
        heatmap_data = heatmap_data.reindex(columns=selected_time_points)  # Reorder the columns
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
        plt.title('Concentrations at Different Time Points by Pd Source and Solvent')

        # Display the heatmap using Streamlit by passing the Matplotlib figure
        st.pyplot(plt.gcf())  # Pass the current figure (gcf)
    else:
        st.warning("Please select data")


def generate_colors(num_colors):
    # Define a list of color codes (you can customize this list)
    color_list = ['#F7941D', '#426386', '#FACA6E', '#ff5733', '#995577', '#2299aa', '#ffcc22', '#1199dd']
    
    # Repeat the color list to cover all bars
    colors = [color_list[i % len(color_list)] for i in range(num_colors)]
    
    return colors

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
        plot_bgcolor="rgba(0, 0, 0, 0)",
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


def create_scatter_plot(df):
    # Select columns for X-axis and Y-axis
    x_axis_options = [col for col in df.columns if not any(exclude in col for exclude in ["SM", "Pdt", "Im", "Unnamed"])]
    y_axis_options = [col for col in df.columns if "SM" in col or "Pdt" in col]
    x_axis = st.sidebar.selectbox("Select X-axis Column", x_axis_options)
    y_axis = st.sidebar.selectbox("Select Y-axis Column", y_axis_options)
    # Select columns for hue, size, etc.
    # Exclude the selected x_axis from hue and size options
    available_columns = [col for col in x_axis_options if col not in x_axis and col != 'Temp']
    hue_column = st.sidebar.selectbox("Select Hue Column", available_columns)
    size_column_var = [c for c in available_columns if c != hue_column]
    size_column = st.sidebar.selectbox("Select Size Column", ['Temp'])
    # Create scatter plot
    fig = px.scatter(
        df,
        x=x_axis,
        y=y_axis,
        color=hue_column,
        size=size_column,
        title=f"Scatter Plot: {x_axis} vs {y_axis}",
    )

    fig.update_layout(
        xaxis_title=x_axis,
        yaxis_title=y_axis,
        showlegend=True,
        legend_title=hue_column,
        legend=dict(
            x=1.02,  # Adjust the legend position
        ),
        margin=dict(l=0, r=50, b=50, t=50),  # Adjust the margins as needed
        width=800,
        height=600,
        xaxis_showgrid=False,  # Remove x-axis grid lines
        yaxis_showgrid=False,
        plot_bgcolor="rgba(0, 0, 0, 0)",
    )

    # # Show the plot
    st.plotly_chart(fig)
