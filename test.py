import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import io

# Sample data
data = pd.DataFrame({
    'X': [1, 2, 3, 4, 5],
    'Y': [10, 12, 8, 15, 11],
    'Category': ['A', 'B', 'A', 'B', 'A']
})

# Title and Description
st.title("Interactive Data Plotting App")
st.write("Upload a CSV file to generate various plots or use the sample data below.")

# Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    data = pd.read_csv(uploaded_file)

# Display the uploaded data
st.subheader("Uploaded Data:")
st.write(data)

# Create tabs for different plots
tabs = st.tabs(["Scatter Plot", "Bar Chart", "Line Chart"])

# Scatter Plot Tab
with tabs[0]:
    st.subheader("Scatter Plot")
    x_axis = st.selectbox("X-axis:", data.columns)
    y_axis = st.selectbox("Y-axis:", data.columns)

    # Create a scatter plot using Matplotlib
    fig, ax = plt.subplots()
    ax.scatter(data[x_axis], data[y_axis])
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    st.pyplot(fig)

# Bar Chart Tab
with tabs[1]:
    st.subheader("Bar Chart")
    x_axis_bar = st.selectbox("X-axis (Bar):", data.columns)
    y_axis_bar = st.selectbox("Y-axis (Bar):", data.columns)
    bar_chart = data.plot.bar(x=x_axis_bar, y=y_axis_bar)
    st.pyplot(bar_chart)

# Line Chart Tab
with tabs[2]:
    st.subheader("Line Chart")
    x_axis_line = st.selectbox("X-axis (Line):", data.columns)
    y_axis_line = st.selectbox("Y-axis (Line):", data.columns)
    line_chart = px.line(data, x=x_axis_line, y=y_axis_line)
    st.plotly_chart(line_chart)
