import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add parent directory to path to import utils.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_data, create_bar_chart, create_pie_chart, create_donut_chart, format_currency, generate_insights

def show(uploaded_file=None, use_sample=True):
    """Display the This Year view of budget data"""
    # Page header
    st.markdown('<div class="main-header">This Year\'s Budget</div>', unsafe_allow_html=True)
    
    # Load data
    data = load_data(uploaded_file, use_sample)
    
    if data is None:
        st.error("No data available. Please upload a file or use sample data.")
        return
    
    # Get the current year (latest year in the data)
    current_year = max(data.keys())
    
    # Display current year in the header
    st.markdown(f'<div class="sub-header">Budget Analysis for {current_year}</div>', unsafe_allow_html=True)
    
    # Get data for the current year
    year_data = data[current_year]
    
    # Create tabs for different sections
    tabs = st.tabs(["Key Stats", "Ministry Allocations", "Sector-wise Expenditure", "Revenue Sources", "Capital vs Revenue"])
    
    # Tab 1: Key Stats
    with tabs[0]:
        st.markdown('<div class="section-header">Budget Summary</div>', unsafe_allow_html=True)
        
        # Display key stats in a grid
        summary = year_data['budget_summary']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Budget", format_currency(summary['Total Budget'] * 1e7))
            st.metric("GDP", format_currency(summary['GDP'] * 1e7))
        
        with col2:
            st.metric("Fiscal Deficit", format_currency(summary['Fiscal Deficit'] * 1e7))
            st.metric("Fiscal Deficit %", f"{summary['Fiscal Deficit %']}% of GDP")
        
        with col3:
            st.metric("Revenue Deficit", format_currency(summary['Revenue Deficit'] * 1e7))
            st.metric("Revenue Deficit %", f"{summary['Revenue Deficit %']}% of GDP")
        
        # Insights
        st.markdown('<div class="section-header">Insights</div>', unsafe_allow_html=True)
        
        insights = generate_insights(data, current_year)
        
        with st.container():
            for insight in insights:
                st.markdown(f"• {insight}")
    
    # Tab 2: Ministry Allocations
    with tabs[1]:
        st.markdown('<div class="section-header">Ministry-wise Budget Allocation</div>', unsafe_allow_html=True)
        
        ministry_df = year_data['ministry_allocation'].sort_values('Allocation (in Crores)', ascending=False)
        
        # Display ministry allocation table
        st.dataframe(
            ministry_df.style.format({
                'Allocation (in Crores)': lambda x: format_currency(x * 1e7)
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # Display horizontal bar chart
        ministry_fig = create_bar_chart(
            ministry_df, 
            'Ministry', 
            'Allocation (in Crores)', 
            f"Ministry-wise Budget Allocation ({current_year})",
            horizontal=True
        )
        st.plotly_chart(ministry_fig, use_container_width=True)
        
        # Display pie chart
        ministry_pie = create_pie_chart(
            ministry_df,
            'Allocation (in Crores)',
            'Ministry',
            f"Proportion of Budget Allocation by Ministry ({current_year})"
        )
        st.plotly_chart(ministry_pie, use_container_width=True)
    
    # Tab 3: Sector-wise Expenditure
    with tabs[2]:
        st.markdown('<div class="section-header">Sector-wise Expenditure</div>', unsafe_allow_html=True)
        
        if 'sector_expenditure' in year_data:
            sector_df = year_data['sector_expenditure'].sort_values('Expenditure (in Crores)', ascending=False)
            
            # Display sector expenditure table
            st.dataframe(
                sector_df.style.format({
                    'Expenditure (in Crores)': lambda x: format_currency(x * 1e7)
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # Display horizontal bar chart
            sector_fig = create_bar_chart(
                sector_df, 
                'Sector', 
                'Expenditure (in Crores)', 
                f"Sector-wise Expenditure ({current_year})",
                horizontal=True
            )
            st.plotly_chart(sector_fig, use_container_width=True)
            
            # Display donut chart
            sector_donut = create_donut_chart(
                sector_df,
                'Expenditure (in Crores)',
                'Sector',
                f"Proportion of Expenditure by Sector ({current_year})"
            )
            st.plotly_chart(sector_donut, use_container_width=True)
        else:
            st.info("Sector-wise expenditure data not available for this year.")
    
    # Tab 4: Revenue Sources
    with tabs[3]:
        st.markdown('<div class="section-header">Revenue Sources</div>', unsafe_allow_html=True)
        
        if 'revenue_sources' in year_data:
            revenue_df = year_data['revenue_sources'].sort_values('Amount (in Crores)', ascending=False)
            
            # Display revenue sources table
            st.dataframe(
                revenue_df.style.format({
                    'Amount (in Crores)': lambda x: format_currency(x * 1e7)
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # Display bar chart
            revenue_fig = create_bar_chart(
                revenue_df, 
                'Source', 
                'Amount (in Crores)', 
                f"Revenue Sources ({current_year})"
            )
            st.plotly_chart(revenue_fig, use_container_width=True)
            
            # Display pie chart
            revenue_pie = create_pie_chart(
                revenue_df,
                'Amount (in Crores)',
                'Source',
                f"Proportion of Revenue by Source ({current_year})"
            )
            st.plotly_chart(revenue_pie, use_container_width=True)
        else:
            st.info("Revenue sources data not available for this year.")
    
    # Tab 5: Capital vs Revenue Expenditure
    with tabs[4]:
        st.markdown('<div class="section-header">Capital vs Revenue Expenditure</div>', unsafe_allow_html=True)
        
        if 'spending_type' in year_data:
            spending_df = year_data['spending_type']
            
            # Display spending type table
            st.dataframe(
                spending_df.style.format({
                    'Amount (in Crores)': lambda x: format_currency(x * 1e7)
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # Display pie chart
            spending_pie = create_pie_chart(
                spending_df,
                'Amount (in Crores)',
                'Type',
                f"Capital vs Revenue Expenditure ({current_year})"
            )
            st.plotly_chart(spending_pie, use_container_width=True)
            
            # Calculate percentages
            total = spending_df['Amount (in Crores)'].sum()
            spending_df['Percentage'] = (spending_df['Amount (in Crores)'] / total) * 100
            
            # Create a gauge chart
            capital_percentage = spending_df.loc[spending_df['Type'] == 'Capital Expenditure', 'Percentage'].iloc[0]
            
            gauge_fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = capital_percentage,
                title = {'text': "Capital Expenditure (% of Total)"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "royalblue"},
                    'steps': [
                        {'range': [0, 20], 'color': "lightcoral"},
                        {'range': [20, 40], 'color': "lightsalmon"},
                        {'range': [40, 60], 'color': "lightgreen"},
                        {'range': [60, 80], 'color': "mediumseagreen"},
                        {'range': [80, 100], 'color': "seagreen"}
                    ]
                }
            ))
            
            st.plotly_chart(gauge_fig, use_container_width=True)
        else:
            st.info("Capital vs Revenue expenditure data not available for this year.") 