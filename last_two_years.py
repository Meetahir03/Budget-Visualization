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
    """Display the Last 2 Years view of budget data"""
    # Page header
    st.markdown('<div class="main-header">Last 2 Years\' Budget</div>', unsafe_allow_html=True)
    
    # Load data
    data = load_data(uploaded_file, use_sample)
    
    if data is None:
        st.error("No data available. Please upload a file or use sample data.")
        return
    
    # Get the last 2 years (latest 2 years in the data)
    years = sorted(data.keys(), reverse=True)
    if len(years) < 2:
        st.warning("Data for at least 2 years is required for this view. Currently only data for 1 year is available.")
        return
    
    selected_years = years[:2]
    
    # Display selected years in the header
    st.markdown(f'<div class="sub-header">Budget Comparison: {selected_years[0]} vs {selected_years[1]}</div>', unsafe_allow_html=True)
    
    # Create tabs for different sections
    tabs = st.tabs(["Key Stats", "Ministry Allocations", "Sector-wise Expenditure", "Revenue Sources", "Capital vs Revenue"])
    
    # Tab 1: Key Stats
    with tabs[0]:
        st.markdown('<div class="section-header">Budget Summary Comparison</div>', unsafe_allow_html=True)
        
        # Display key stats comparison in a grid
        col1, col2 = st.columns(2)
        
        # Year 1 (Current Year)
        with col1:
            st.subheader(f"{selected_years[0]}")
            summary1 = data[selected_years[0]]['budget_summary']
            
            st.metric("Total Budget", format_currency(summary1['Total Budget'] * 1e7))
            st.metric("Fiscal Deficit", format_currency(summary1['Fiscal Deficit'] * 1e7))
            st.metric("Fiscal Deficit %", f"{summary1['Fiscal Deficit %']}% of GDP")
            st.metric("GDP", format_currency(summary1['GDP'] * 1e7))
        
        # Year 2 (Previous Year)
        with col2:
            st.subheader(f"{selected_years[1]}")
            summary2 = data[selected_years[1]]['budget_summary']
            
            # Calculate percentage change
            budget_change = ((summary1['Total Budget'] - summary2['Total Budget']) / summary2['Total Budget']) * 100
            deficit_change = ((summary1['Fiscal Deficit'] - summary2['Fiscal Deficit']) / summary2['Fiscal Deficit']) * 100
            gdp_change = ((summary1['GDP'] - summary2['GDP']) / summary2['GDP']) * 100
            
            st.metric("Total Budget", format_currency(summary2['Total Budget'] * 1e7), delta=f"{budget_change:.2f}%")
            st.metric("Fiscal Deficit", format_currency(summary2['Fiscal Deficit'] * 1e7), delta=f"{deficit_change:.2f}%")
            st.metric("Fiscal Deficit %", f"{summary2['Fiscal Deficit %']}% of GDP", delta=f"{summary1['Fiscal Deficit %'] - summary2['Fiscal Deficit %']:.2f}%")
            st.metric("GDP", format_currency(summary2['GDP'] * 1e7), delta=f"{gdp_change:.2f}%")
        
        # Line chart for total budget trend
        st.markdown('<div class="section-header">Budget Trend</div>', unsafe_allow_html=True)
        
        budget_trend = [data[year]['budget_summary']['Total Budget'] for year in selected_years]
        budget_trend.reverse()  # Reverse for chronological order
        
        budget_fig = create_line_chart(
            selected_years[::-1],  # Reverse for chronological order
            budget_trend,
            "Total Budget Trend",
            {"x": "Year", "y": "Budget (in Crores)"}
        )
        st.plotly_chart(budget_fig, use_container_width=True)
        
        # Line chart for fiscal deficit trend
        deficit_trend = [data[year]['budget_summary']['Fiscal Deficit'] for year in selected_years]
        deficit_trend.reverse()  # Reverse for chronological order
        
        deficit_fig = create_line_chart(
            selected_years[::-1],  # Reverse for chronological order
            deficit_trend,
            "Fiscal Deficit Trend",
            {"x": "Year", "y": "Deficit (in Crores)"}
        )
        st.plotly_chart(deficit_fig, use_container_width=True)
        
        # Insights
        st.markdown('<div class="section-header">Key Insights</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown(f"• The total budget has {'increased' if budget_change > 0 else 'decreased'} by {abs(budget_change):.2f}% from {selected_years[1]} to {selected_years[0]}.")
            st.markdown(f"• The fiscal deficit has {'increased' if deficit_change > 0 else 'decreased'} by {abs(deficit_change):.2f}% from {selected_years[1]} to {selected_years[0]}.")
            st.markdown(f"• The fiscal deficit as percentage of GDP has {'increased' if (summary1['Fiscal Deficit %'] - summary2['Fiscal Deficit %']) > 0 else 'decreased'} by {abs(summary1['Fiscal Deficit %'] - summary2['Fiscal Deficit %']):.2f}% points.")
            st.markdown(f"• The GDP has {'increased' if gdp_change > 0 else 'decreased'} by {abs(gdp_change):.2f}% from {selected_years[1]} to {selected_years[0]}.")
    
    # Tab 2: Ministry Allocations
    with tabs[1]:
        st.markdown('<div class="section-header">Ministry-wise Budget Allocation Comparison</div>', unsafe_allow_html=True)
        
        # Get ministry allocation dataframes for both years
        ministry_df1 = data[selected_years[0]]['ministry_allocation']
        ministry_df2 = data[selected_years[1]]['ministry_allocation']
        
        # Merge the two dataframes
        merged_ministry_df = pd.merge(
            ministry_df1, ministry_df2,
            on='Ministry',
            suffixes=(f' ({selected_years[0]})', f' ({selected_years[1]})'),
            how='outer'
        ).fillna(0)
        
        # Calculate change
        merged_ministry_df['Change (%)'] = ((merged_ministry_df[f'Allocation (in Crores) ({selected_years[0]})'] - 
                                            merged_ministry_df[f'Allocation (in Crores) ({selected_years[1]})']) / 
                                            merged_ministry_df[f'Allocation (in Crores) ({selected_years[1]})'] * 100)
        
        # Sort by current year's allocation
        merged_ministry_df = merged_ministry_df.sort_values(f'Allocation (in Crores) ({selected_years[0]})', ascending=False)
        
        # Display merged table
        st.dataframe(
            merged_ministry_df.style.format({
                f'Allocation (in Crores) ({selected_years[0]})': lambda x: format_currency(x * 1e7),
                f'Allocation (in Crores) ({selected_years[1]})': lambda x: format_currency(x * 1e7),
                'Change (%)': '{:.2f}%'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # Create a grouped bar chart for comparison
        ministry_comp_df = pd.DataFrame({
            'Ministry': ministry_df1['Ministry'],
            f'{selected_years[0]}': ministry_df1['Allocation (in Crores)'],
            f'{selected_years[1]}': pd.Series(
                ministry_df2.set_index('Ministry').loc[ministry_df1['Ministry'], 'Allocation (in Crores)'],
                index=ministry_df1.index
            ).fillna(0)
        })
        
        # Reshape for Plotly
        ministry_comp_long = ministry_comp_df.melt(
            id_vars=['Ministry'],
            value_vars=[f'{selected_years[0]}', f'{selected_years[1]}'],
            var_name='Year',
            value_name='Allocation (in Crores)'
        )
        
        # Create grouped bar chart
        fig = px.bar(
            ministry_comp_long, 
            x='Ministry', 
            y='Allocation (in Crores)',
            color='Year',
            barmode='group',
            title=f"Ministry-wise Budget Allocation: {selected_years[0]} vs {selected_years[1]}",
            height=500
        )
        
        fig.update_layout(
            title_font_size=20,
            xaxis_title_font_size=16,
            yaxis_title_font_size=16,
            legend_title_font_size=16,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Top 5 ministries with highest increase
        st.markdown('<div class="section-header">Top 5 Ministries with Highest Budget Increase</div>', unsafe_allow_html=True)
        
        top_increase = merged_ministry_df.sort_values('Change (%)', ascending=False).head(5)
        
        fig_increase = px.bar(
            top_increase,
            x='Ministry',
            y='Change (%)',
            title=f"Top 5 Ministries with Highest Budget Increase ({selected_years[1]} to {selected_years[0]})",
            color='Change (%)',
            color_continuous_scale='Greens',
            height=400
        )
        
        fig_increase.update_layout(
            title_font_size=20,
            xaxis_title_font_size=16,
            yaxis_title_font_size=16
        )
        
        st.plotly_chart(fig_increase, use_container_width=True)
    
    # Tab 3: Sector-wise Expenditure
    with tabs[2]:
        st.markdown('<div class="section-header">Sector-wise Expenditure Comparison</div>', unsafe_allow_html=True)
        
        # Check if sector data is available for both years
        if 'sector_expenditure' in data[selected_years[0]] and 'sector_expenditure' in data[selected_years[1]]:
            # Get sector expenditure dataframes for both years
            sector_df1 = data[selected_years[0]]['sector_expenditure']
            sector_df2 = data[selected_years[1]]['sector_expenditure']
            
            # Merge the two dataframes
            merged_sector_df = pd.merge(
                sector_df1, sector_df2,
                on='Sector',
                suffixes=(f' ({selected_years[0]})', f' ({selected_years[1]})'),
                how='outer'
            ).fillna(0)
            
            # Calculate change
            merged_sector_df['Change (%)'] = ((merged_sector_df[f'Expenditure (in Crores) ({selected_years[0]})'] - 
                                              merged_sector_df[f'Expenditure (in Crores) ({selected_years[1]})']) / 
                                              merged_sector_df[f'Expenditure (in Crores) ({selected_years[1]})'] * 100)
            
            # Sort by current year's expenditure
            merged_sector_df = merged_sector_df.sort_values(f'Expenditure (in Crores) ({selected_years[0]})', ascending=False)
            
            # Display merged table
            st.dataframe(
                merged_sector_df.style.format({
                    f'Expenditure (in Crores) ({selected_years[0]})': lambda x: format_currency(x * 1e7),
                    f'Expenditure (in Crores) ({selected_years[1]})': lambda x: format_currency(x * 1e7),
                    'Change (%)': '{:.2f}%'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # Create a grouped bar chart for comparison
            sector_comp_df = pd.DataFrame({
                'Sector': sector_df1['Sector'],
                f'{selected_years[0]}': sector_df1['Expenditure (in Crores)'],
                f'{selected_years[1]}': pd.Series(
                    sector_df2.set_index('Sector').loc[sector_df1['Sector'], 'Expenditure (in Crores)'],
                    index=sector_df1.index
                ).fillna(0)
            })
            
            # Reshape for Plotly
            sector_comp_long = sector_comp_df.melt(
                id_vars=['Sector'],
                value_vars=[f'{selected_years[0]}', f'{selected_years[1]}'],
                var_name='Year',
                value_name='Expenditure (in Crores)'
            )
            
            # Create grouped bar chart
            fig = px.bar(
                sector_comp_long, 
                x='Sector', 
                y='Expenditure (in Crores)',
                color='Year',
                barmode='group',
                title=f"Sector-wise Expenditure: {selected_years[0]} vs {selected_years[1]}",
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
            st.info("Sector-wise expenditure data not available for comparison.")
    
    # Tab 4: Revenue Sources
    with tabs[3]:
        st.markdown('<div class="section-header">Revenue Sources Comparison</div>', unsafe_allow_html=True)
        
        # Check if revenue data is available for both years
        if 'revenue_sources' in data[selected_years[0]] and 'revenue_sources' in data[selected_years[1]]:
            # Get revenue sources dataframes for both years
            revenue_df1 = data[selected_years[0]]['revenue_sources']
            revenue_df2 = data[selected_years[1]]['revenue_sources']
            
            # Merge the two dataframes
            merged_revenue_df = pd.merge(
                revenue_df1, revenue_df2,
                on='Source',
                suffixes=(f' ({selected_years[0]})', f' ({selected_years[1]})'),
                how='outer'
            ).fillna(0)
            
            # Calculate change
            merged_revenue_df['Change (%)'] = ((merged_revenue_df[f'Amount (in Crores) ({selected_years[0]})'] - 
                                               merged_revenue_df[f'Amount (in Crores) ({selected_years[1]})']) / 
                                               merged_revenue_df[f'Amount (in Crores) ({selected_years[1]})'] * 100)
            
            # Sort by current year's amount
            merged_revenue_df = merged_revenue_df.sort_values(f'Amount (in Crores) ({selected_years[0]})', ascending=False)
            
            # Display merged table
            st.dataframe(
                merged_revenue_df.style.format({
                    f'Amount (in Crores) ({selected_years[0]})': lambda x: format_currency(x * 1e7),
                    f'Amount (in Crores) ({selected_years[1]})': lambda x: format_currency(x * 1e7),
                    'Change (%)': '{:.2f}%'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # Create a grouped bar chart for comparison
            revenue_comp_df = pd.DataFrame({
                'Source': revenue_df1['Source'],
                f'{selected_years[0]}': revenue_df1['Amount (in Crores)'],
                f'{selected_years[1]}': pd.Series(
                    revenue_df2.set_index('Source').loc[revenue_df1['Source'], 'Amount (in Crores)'],
                    index=revenue_df1.index
                ).fillna(0)
            })
            
            # Reshape for Plotly
            revenue_comp_long = revenue_comp_df.melt(
                id_vars=['Source'],
                value_vars=[f'{selected_years[0]}', f'{selected_years[1]}'],
                var_name='Year',
                value_name='Amount (in Crores)'
            )
            
            # Create grouped bar chart
            fig = px.bar(
                revenue_comp_long, 
                x='Source', 
                y='Amount (in Crores)',
                color='Year',
                barmode='group',
                title=f"Revenue Sources: {selected_years[0]} vs {selected_years[1]}",
                height=500
            )
            
            fig.update_layout(
                title_font_size=20,
                xaxis_title_font_size=16,
                yaxis_title_font_size=16,
                legend_title_font_size=16,
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Revenue sources data not available for comparison.")
    
    # Tab 5: Capital vs Revenue Expenditure
    with tabs[4]:
        st.markdown('<div class="section-header">Capital vs Revenue Expenditure Comparison</div>', unsafe_allow_html=True)
        
        # Check if spending type data is available for both years
        if 'spending_type' in data[selected_years[0]] and 'spending_type' in data[selected_years[1]]:
            # Get spending type dataframes for both years
            spending_df1 = data[selected_years[0]]['spending_type']
            spending_df2 = data[selected_years[1]]['spending_type']
            
            # Create a dataframe for comparison
            spending_comp = pd.DataFrame({
                'Type': ['Capital Expenditure', 'Revenue Expenditure'],
                f'{selected_years[0]}': [
                    spending_df1.loc[spending_df1['Type'] == 'Capital Expenditure', 'Amount (in Crores)'].iloc[0],
                    spending_df1.loc[spending_df1['Type'] == 'Revenue Expenditure', 'Amount (in Crores)'].iloc[0]
                ],
                f'{selected_years[1]}': [
                    spending_df2.loc[spending_df2['Type'] == 'Capital Expenditure', 'Amount (in Crores)'].iloc[0],
                    spending_df2.loc[spending_df2['Type'] == 'Revenue Expenditure', 'Amount (in Crores)'].iloc[0]
                ]
            })
            
            # Calculate changes
            spending_comp['Change (%)'] = ((spending_comp[f'{selected_years[0]}'] - spending_comp[f'{selected_years[1]}']) / 
                                           spending_comp[f'{selected_years[1]}'] * 100)
            
            # Display comparison table
            st.dataframe(
                spending_comp.style.format({
                    f'{selected_years[0]}': lambda x: format_currency(x * 1e7),
                    f'{selected_years[1]}': lambda x: format_currency(x * 1e7),
                    'Change (%)': '{:.2f}%'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # Create a grouped bar chart for comparison
            # Reshape for Plotly
            spending_comp_long = spending_comp.melt(
                id_vars=['Type'],
                value_vars=[f'{selected_years[0]}', f'{selected_years[1]}'],
                var_name='Year',
                value_name='Amount (in Crores)'
            )
            
            # Create grouped bar chart
            fig = px.bar(
                spending_comp_long, 
                x='Type', 
                y='Amount (in Crores)',
                color='Year',
                barmode='group',
                title=f"Capital vs Revenue Expenditure: {selected_years[0]} vs {selected_years[1]}",
                height=400
            )
            
            fig.update_layout(
                title_font_size=20,
                xaxis_title_font_size=16,
                yaxis_title_font_size=16,
                legend_title_font_size=16
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Calculate percentages for both years
            total1 = spending_df1['Amount (in Crores)'].sum()
            total2 = spending_df2['Amount (in Crores)'].sum()
            
            capital_pct1 = (spending_df1.loc[spending_df1['Type'] == 'Capital Expenditure', 'Amount (in Crores)'].iloc[0] / total1) * 100
            capital_pct2 = (spending_df2.loc[spending_df2['Type'] == 'Capital Expenditure', 'Amount (in Crores)'].iloc[0] / total2) * 100
            
            revenue_pct1 = (spending_df1.loc[spending_df1['Type'] == 'Revenue Expenditure', 'Amount (in Crores)'].iloc[0] / total1) * 100
            revenue_pct2 = (spending_df2.loc[spending_df2['Type'] == 'Revenue Expenditure', 'Amount (in Crores)'].iloc[0] / total2) * 100
            
            # Display percentage changes
            st.markdown(f"### Capital Expenditure as % of Total Expenditure")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(f"{selected_years[0]}", f"{capital_pct1:.2f}%")
            
            with col2:
                st.metric(f"{selected_years[1]}", f"{capital_pct2:.2f}%", delta=f"{capital_pct1 - capital_pct2:.2f}%")
            
            st.markdown(f"### Revenue Expenditure as % of Total Expenditure")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(f"{selected_years[0]}", f"{revenue_pct1:.2f}%")
            
            with col2:
                st.metric(f"{selected_years[1]}", f"{revenue_pct2:.2f}%", delta=f"{revenue_pct1 - revenue_pct2:.2f}%")
        else:
            st.info("Capital vs Revenue expenditure data not available for comparison.") 