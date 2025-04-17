import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt
from pages import this_year, last_two_years, last_three_years

# Set page configuration
st.set_page_config(
    page_title="Wallet of India - Budget Visualization",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #FF9933;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #138808;
        text-align: center;
        margin-bottom: 30px;
    }
    .section-header {
        font-size: 20px;
        font-weight: bold;
        color: #000080;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .insight-box {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown('<div class="main-header">Wallet of India</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sub-header">Budget Visualization</div>', unsafe_allow_html=True)

# Navigation
st.sidebar.markdown("## Navigation")
page = st.sidebar.radio("Select a View:", 
                        ["Home", "This Year", "Last 2 Years", "Last 3 Years"])

# File uploader in sidebar
st.sidebar.markdown("## Upload Budget Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file:", 
                                          type=["csv", "xlsx"])

# Sample data option
if st.sidebar.checkbox("Use Sample Data", value=True):
    sample_data = True
else:
    sample_data = False

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "Wallet of India is a visualization tool for the Indian Union Budget. "
    "It aims to present complex budget data in a simple, intuitive, and interactive format."
)
st.sidebar.markdown("© 2025 Wallet of India")

# Main content
if page == "Home":
    # Homepage content
    st.markdown('<div class="main-header">Wallet of India</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Visualizing the Indian Union Budget</div>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    Welcome to **Wallet of India**, an interactive platform that simplifies and visualizes the Indian Union Budget. 
    This tool aims to make national-level financial data accessible and understandable to everyone.
    
    ### Features:
    - **Three main views**: This Year, Last 2 Years, and Last 3 Years
    - **Interactive visualizations**: Bar charts, pie charts, line charts, and donut charts
    - **Comprehensive analysis**: Ministry-wise allocations, sector-wise expenditure, revenue sources, and more
    - **Custom data upload**: Analyze your own budget data or other countries' budgets
    
    ### How to use:
    1. Select a view from the sidebar
    2. Upload your own data or use our sample data
    3. Explore the visualizations and insights
    
    Get started by selecting a view from the sidebar!
    """)
    
    # Display sample images
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Sample Visualization: Sector-wise Allocation</div>', unsafe_allow_html=True)
        # Generate a sample pie chart
        labels = ['Healthcare', 'Education', 'Defense', 'Infrastructure', 'Agriculture', 'Others']
        values = [20, 15, 25, 18, 12, 10]
        
        fig = px.pie(values=values, names=labels, title="Sector-wise Budget Allocation")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">Sample Visualization: Budget Trends</div>', unsafe_allow_html=True)
        # Generate a sample line chart
        years = [2020, 2021, 2022, 2023, 2024]
        budget = [30000, 32500, 35000, 38000, 40000]
        
        fig = px.line(x=years, y=budget, markers=True, 
                    labels={"x": "Year", "y": "Budget (in Crores)"},
                    title="Budget Trend Analysis")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

elif page == "This Year":
    this_year.show(uploaded_file, sample_data)
    
elif page == "Last 2 Years":
    last_two_years.show(uploaded_file, sample_data)
    
elif page == "Last 3 Years":
    last_three_years.show(uploaded_file, sample_data) 