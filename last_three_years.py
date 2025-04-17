import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import sys
import os

# Add parent directory to path to import utils.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_data, create_bar_chart, create_line_chart, format_currency, generate_insights

def show(uploaded_file=None, use_sample=True):
    """Display the Last 3 Years view of budget data"""
    # Page header
    st.markdown('<div class="main-header">Last 3 Years\' Budget</div>', unsafe_allow_html=True)
    
    # Load data
    data = load_data(uploaded_file, use_sample)
    
    if data is None:
        st.error("No data available. Please upload a file or use sample data.")
        return
    
    # Get the last 3 years (latest 3 years in the data)
    years = sorted(data.keys(), reverse=True)
    if len(years) < 3:
        st.warning(f"Data for at least 3 years is required for this view. Currently only data for {len(years)} year(s) is available.")
        return
    
    selected_years = years[:3]
    
    # Display selected years in the header
    st.markdown(f'<div class="sub-header">Budget Analysis: {selected_years[0]} - {selected_years[2]}</div>', unsafe_allow_html=True)
    
    # Create tabs for different sections
    tabs = st.tabs(["Budget Trends", "Ministry Allocations", "Sector Trends", "Revenue Trends"])
    
    # Tab 1: Budget Trends
    with tabs[0]:
        st.markdown('<div class="section-header">Budget Summary Trends</div>', unsafe_allow_html=True)
        
        # Create dataframe for budget summary
        summary_data = {
            'Year': selected_years,
            'Total Budget': [data[year]['budget_summary']['Total Budget'] for year in selected_years],
            'Fiscal Deficit': [data[year]['budget_summary']['Fiscal Deficit'] for year in selected_years],
            'Fiscal Deficit %': [data[year]['budget_summary']['Fiscal Deficit %'] for year in selected_years],
            'GDP': [data[year]['budget_summary']['GDP'] for year in selected_years]
        }
        
        summary_df = pd.DataFrame(summary_data)
        
        # Display summary table
        st.dataframe(
            summary_df.style.format({
                'Total Budget': lambda x: format_currency(x * 1e7),
                'Fiscal Deficit': lambda x: format_currency(x * 1e7),
                'Fiscal Deficit %': '{:.2f}%',
                'GDP': lambda x: format_currency(x * 1e7)
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # Line charts for key metrics
        col1, col2 = st.columns(2)
        
        with col1:
            # Total Budget Trend
            budget_trend = summary_df.sort_values('Year')
            budget_fig = create_line_chart(
                budget_trend['Year'],
                budget_trend['Total Budget'],
                "Total Budget Trend",
                {"x": "Year", "y": "Budget (in Crores)"}
            )
            st.plotly_chart(budget_fig, use_container_width=True)
            
            # GDP Trend
            gdp_fig = create_line_chart(
                budget_trend['Year'],
                budget_trend['GDP'],
                "GDP Trend",
                {"x": "Year", "y": "GDP (in Crores)"}
            )
            st.plotly_chart(gdp_fig, use_container_width=True)
        
        with col2:
            # Fiscal Deficit Trend
            deficit_fig = create_line_chart(
                budget_trend['Year'],
                budget_trend['Fiscal Deficit'],
                "Fiscal Deficit Trend",
                {"x": "Year", "y": "Deficit (in Crores)"}
            )
            st.plotly_chart(deficit_fig, use_container_width=True)
            
            # Fiscal Deficit % Trend
            deficit_pct_fig = create_line_chart(
                budget_trend['Year'],
                budget_trend['Fiscal Deficit %'],
                "Fiscal Deficit % of GDP Trend",
                {"x": "Year", "y": "Deficit (% of GDP)"}
            )
            st.plotly_chart(deficit_pct_fig, use_container_width=True)
        
        # Overall growth statistics
        st.markdown('<div class="section-header">Overall Growth</div>', unsafe_allow_html=True)
        
        # Calculate CAGR (Compound Annual Growth Rate)
        years_diff = selected_years[0] - selected_years[-1]
        budget_cagr = ((summary_df.iloc[0]['Total Budget'] / summary_df.iloc[-1]['Total Budget']) ** (1/years_diff) - 1) * 100
        gdp_cagr = ((summary_df.iloc[0]['GDP'] / summary_df.iloc[-1]['GDP']) ** (1/years_diff) - 1) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Budget CAGR", f"{budget_cagr:.2f}%")
            st.metric("Total Budget Growth", 
                    f"{((summary_df.iloc[0]['Total Budget'] - summary_df.iloc[-1]['Total Budget']) / summary_df.iloc[-1]['Total Budget'] * 100):.2f}%")
        
        with col2:
            st.metric("GDP CAGR", f"{gdp_cagr:.2f}%")
            st.metric("Total GDP Growth", 
                    f"{((summary_df.iloc[0]['GDP'] - summary_df.iloc[-1]['GDP']) / summary_df.iloc[-1]['GDP'] * 100):.2f}%")
    
    # Tab 2: Ministry Allocations
    with tabs[1]:
        st.markdown('<div class="section-header">Ministry Allocation Trends</div>', unsafe_allow_html=True)
        
        # Combine ministry data for all years
        ministry_data = []
        for year in selected_years:
            year_df = data[year]['ministry_allocation']
            year_df['Year'] = year
            ministry_data.append(year_df)
        
        all_ministry_df = pd.concat(ministry_data)
        
        # Select ministry for detailed analysis
        all_ministries = sorted(all_ministry_df['Ministry'].unique())
        selected_ministry = st.selectbox("Select a Ministry for Detailed Analysis", all_ministries)
        
        # Filter for selected ministry
        ministry_trend = all_ministry_df[all_ministry_df['Ministry'] == selected_ministry]
        
        # Sort by year
        ministry_trend = ministry_trend.sort_values('Year')
        
        # Display trend for selected ministry
        st.subheader(f"{selected_ministry} Budget Allocation Trend")
        
        ministry_fig = create_line_chart(
            ministry_trend['Year'],
            ministry_trend['Allocation (in Crores)'],
            f"{selected_ministry} Budget Allocation Trend",
            {"x": "Year", "y": "Allocation (in Crores)"}
        )
        st.plotly_chart(ministry_fig, use_container_width=True)
        
        # Calculate growth
        first_allocation = ministry_trend.iloc[-1]['Allocation (in Crores)']
        last_allocation = ministry_trend.iloc[0]['Allocation (in Crores)']
        growth_pct = ((last_allocation - first_allocation) / first_allocation) * 100
        
        st.metric(
            f"Total Growth ({selected_years[-1]} to {selected_years[0]})", 
            f"{growth_pct:.2f}%"
        )
        
        # Show bar chart for all ministries for the most recent year
        st.subheader(f"All Ministries - {selected_years[0]} Budget Allocation")
        
        latest_ministries = data[selected_years[0]]['ministry_allocation'].sort_values('Allocation (in Crores)', ascending=False)
        
        ministry_bar = create_bar_chart(
            latest_ministries,
            'Ministry',
            'Allocation (in Crores)',
            f"Ministry-wise Budget Allocation ({selected_years[0]})",
            horizontal=True
        )
        st.plotly_chart(ministry_bar, use_container_width=True)
    
    # Tab 3: Sector Trends
    with tabs[2]:
        st.markdown('<div class="section-header">Sector Expenditure Trends</div>', unsafe_allow_html=True)
        
        # Check if sector data is available for all years
        if all('sector_expenditure' in data[year] for year in selected_years):
            # Combine sector data for all years
            sector_data = []
            for year in selected_years:
                year_df = data[year]['sector_expenditure']
                year_df['Year'] = year
                sector_data.append(year_df)
            
            all_sector_df = pd.concat(sector_data)
            
            # Select sector for detailed analysis
            all_sectors = sorted(all_sector_df['Sector'].unique())
            selected_sector = st.selectbox("Select a Sector for Detailed Analysis", all_sectors)
            
            # Filter for selected sector
            sector_trend = all_sector_df[all_sector_df['Sector'] == selected_sector]
            
            # Sort by year
            sector_trend = sector_trend.sort_values('Year')
            
            # Display trend for selected sector
            st.subheader(f"{selected_sector} Expenditure Trend")
            
            sector_fig = create_line_chart(
                sector_trend['Year'],
                sector_trend['Expenditure (in Crores)'],
                f"{selected_sector} Expenditure Trend",
                {"x": "Year", "y": "Expenditure (in Crores)"}
            )
            st.plotly_chart(sector_fig, use_container_width=True)
            
            # Calculate growth
            first_expenditure = sector_trend.iloc[-1]['Expenditure (in Crores)']
            last_expenditure = sector_trend.iloc[0]['Expenditure (in Crores)']
            growth_pct = ((last_expenditure - first_expenditure) / first_expenditure) * 100
            
            st.metric(
                f"Total Growth ({selected_years[-1]} to {selected_years[0]})", 
                f"{growth_pct:.2f}%"
            )
            
            # Compare all sectors across years
            st.subheader(f"Sector-wise Expenditure Comparison")
            
            # Prepare data for stacked bar chart
            sector_pivot = all_sector_df.pivot(index='Sector', columns='Year', values='Expenditure (in Crores)').reset_index()
            sector_pivot = sector_pivot.fillna(0)
            
            # Convert to long format for Plotly
            sector_long = sector_pivot.melt(
                id_vars=['Sector'],
                value_vars=selected_years,
                var_name='Year',
                value_name='Expenditure (in Crores)'
            )
            
            # Create stacked bar chart
            fig = px.bar(
                sector_long, 
                x='Year', 
                y='Expenditure (in Crores)', 
                color='Sector', 
                title="Sector-wise Expenditure Across Years",
                height=500
            )
            
            fig.update_layout(
                title_font_size=20,
                xaxis_title_font_size=16,
                yaxis_title_font_size=16,
                legend_title_font_size=16
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sector-wise expenditure data not available for all selected years.")
    
    # Tab 4: Revenue Trends
    with tabs[3]:
        st.markdown('<div class="section-header">Revenue Source Trends</div>', unsafe_allow_html=True)
        
        # Check if revenue data is available for all years
        if all('revenue_sources' in data[year] for year in selected_years):
            # Combine revenue data for all years
            revenue_data = []
            for year in selected_years:
                year_df = data[year]['revenue_sources']
                year_df['Year'] = year
                revenue_data.append(year_df)
            
            all_revenue_df = pd.concat(revenue_data)
            
            # Select revenue source for detailed analysis
            all_sources = sorted(all_revenue_df['Source'].unique())
            selected_source = st.selectbox("Select a Revenue Source for Detailed Analysis", all_sources)
            
            # Filter for selected source
            source_trend = all_revenue_df[all_revenue_df['Source'] == selected_source]
            
            # Sort by year
            source_trend = source_trend.sort_values('Year')
            
            # Display trend for selected source
            st.subheader(f"{selected_source} Revenue Trend")
            
            source_fig = create_line_chart(
                source_trend['Year'],
                source_trend['Amount (in Crores)'],
                f"{selected_source} Revenue Trend",
                {"x": "Year", "y": "Amount (in Crores)"}
            )
            st.plotly_chart(source_fig, use_container_width=True)
            
            # Calculate growth
            first_amount = source_trend.iloc[-1]['Amount (in Crores)']
            last_amount = source_trend.iloc[0]['Amount (in Crores)']
            growth_pct = ((last_amount - first_amount) / first_amount) * 100
            
            st.metric(
                f"Total Growth ({selected_years[-1]} to {selected_years[0]})", 
                f"{growth_pct:.2f}%"
            )
            
            # Area chart showing all revenue sources over time
            st.subheader(f"All Revenue Sources Over Time")
            
            # Prepare data for area chart
            all_revenue_df_sorted = all_revenue_df.sort_values(['Year', 'Source'])
            
            fig = px.area(
                all_revenue_df_sorted, 
                x='Year', 
                y='Amount (in Crores)', 
                color='Source', 
                title="Revenue Sources Trend",
                height=500
            )
            
            fig.update_layout(
                title_font_size=20,
                xaxis_title_font_size=16,
                yaxis_title_font_size=16,
                legend_title_font_size=16
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Calculate total revenue for each year
            yearly_total = all_revenue_df.groupby('Year')['Amount (in Crores)'].sum().reset_index()
            yearly_total = yearly_total.sort_values('Year')
            
            # Display total revenue trend
            st.subheader("Total Revenue Trend")
            
            total_fig = create_line_chart(
                yearly_total['Year'],
                yearly_total['Amount (in Crores)'],
                "Total Revenue Trend",
                {"x": "Year", "y": "Amount (in Crores)"}
            )
            st.plotly_chart(total_fig, use_container_width=True)
        else:
            st.info("Revenue sources data not available for all selected years.")