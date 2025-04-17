import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

def load_data(uploaded_file=None, use_sample=True):
    """
    Load data from uploaded file or use sample data
    Returns a dictionary with dataframes for different years
    """
    data = {}
    
    if uploaded_file is not None:
        # Handle uploaded file
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:  # Excel file
                df = pd.read_excel(uploaded_file)
                
            # Process the dataframe
            data = process_uploaded_data(df)
            return data
        except Exception as e:
            print(f"Error loading uploaded file: {e}")
            # If error in uploaded file, fall back to sample data if selected
            if use_sample:
                return get_sample_data()
            return None
    
    if use_sample:
        return get_sample_data()
    
    return None

def get_sample_data():
    """Generate sample budget data for demonstration"""
    # Create a dictionary to hold budget data for multiple years
    data = {}
    
    # Generate sample data for 2024 (current year)
    data[2024] = {
        'ministry_allocation': pd.DataFrame({
            'Ministry': ['Finance', 'Defense', 'Railways', 'Health', 'Education', 'Agriculture', 'Home Affairs', 'Others'],
            'Allocation (in Crores)': [850000, 620000, 250000, 180000, 150000, 125000, 110000, 215000]
        }),
        
        'sector_expenditure': pd.DataFrame({
            'Sector': ['Social Services', 'Economic Services', 'General Services', 'Defense', 'Subsidies', 'Others'],
            'Expenditure (in Crores)': [720000, 550000, 410000, 620000, 350000, 150000]
        }),
        
        'revenue_sources': pd.DataFrame({
            'Source': ['GST', 'Income Tax', 'Corporate Tax', 'Customs', 'Excise', 'Non-Tax Revenue', 'Others'],
            'Amount (in Crores)': [680000, 580000, 760000, 180000, 210000, 290000, 100000]
        }),
        
        'spending_type': pd.DataFrame({
            'Type': ['Capital Expenditure', 'Revenue Expenditure'],
            'Amount (in Crores)': [750000, 1750000]
        }),
        
        'budget_summary': {
            'Total Budget': 2500000,
            'Fiscal Deficit': 610000,
            'Fiscal Deficit %': 5.8,
            'Revenue Deficit': 380000,
            'Revenue Deficit %': 3.6,
            'GDP': 10500000
        }
    }
    
    # Generate sample data for 2023
    data[2023] = {
        'ministry_allocation': pd.DataFrame({
            'Ministry': ['Finance', 'Defense', 'Railways', 'Health', 'Education', 'Agriculture', 'Home Affairs', 'Others'],
            'Allocation (in Crores)': [780000, 585000, 235000, 170000, 140000, 115000, 100000, 195000]
        }),
        
        'sector_expenditure': pd.DataFrame({
            'Sector': ['Social Services', 'Economic Services', 'General Services', 'Defense', 'Subsidies', 'Others'],
            'Expenditure (in Crores)': [680000, 510000, 390000, 585000, 330000, 135000]
        }),
        
        'revenue_sources': pd.DataFrame({
            'Source': ['GST', 'Income Tax', 'Corporate Tax', 'Customs', 'Excise', 'Non-Tax Revenue', 'Others'],
            'Amount (in Crores)': [620000, 540000, 700000, 170000, 200000, 270000, 80000]
        }),
        
        'spending_type': pd.DataFrame({
            'Type': ['Capital Expenditure', 'Revenue Expenditure'],
            'Amount (in Crores)': [685000, 1635000]
        }),
        
        'budget_summary': {
            'Total Budget': 2320000,
            'Fiscal Deficit': 580000,
            'Fiscal Deficit %': 6.1,
            'Revenue Deficit': 360000,
            'Revenue Deficit %': 3.8,
            'GDP': 9500000
        }
    }
    
    # Generate sample data for 2022
    data[2022] = {
        'ministry_allocation': pd.DataFrame({
            'Ministry': ['Finance', 'Defense', 'Railways', 'Health', 'Education', 'Agriculture', 'Home Affairs', 'Others'],
            'Allocation (in Crores)': [720000, 550000, 215000, 160000, 125000, 105000, 92000, 183000]
        }),
        
        'sector_expenditure': pd.DataFrame({
            'Sector': ['Social Services', 'Economic Services', 'General Services', 'Defense', 'Subsidies', 'Others'],
            'Expenditure (in Crores)': [640000, 480000, 350000, 550000, 300000, 120000]
        }),
        
        'revenue_sources': pd.DataFrame({
            'Source': ['GST', 'Income Tax', 'Corporate Tax', 'Customs', 'Excise', 'Non-Tax Revenue', 'Others'],
            'Amount (in Crores)': [560000, 500000, 650000, 150000, 190000, 240000, 60000]
        }),
        
        'spending_type': pd.DataFrame({
            'Type': ['Capital Expenditure', 'Revenue Expenditure'],
            'Amount (in Crores)': [640000, 1510000]
        }),
        
        'budget_summary': {
            'Total Budget': 2150000,
            'Fiscal Deficit': 550000,
            'Fiscal Deficit %': 6.4,
            'Revenue Deficit': 340000,
            'Revenue Deficit %': 4.0,
            'GDP': 8600000
        }
    }
    
    return data

def process_uploaded_data(df):
    """Process uploaded data to fit the application structure"""
    # This is a placeholder for actual data processing logic
    # In a real application, you would need to adapt this to the structure of the uploaded file
    
    # Here we'll just create a simple structure similar to the sample data
    # Assuming the uploaded file has a 'year' column and necessary budget data columns
    
    data = {}
    
    # Check if the dataframe has a 'Year' column
    if 'Year' in df.columns:
        years = df['Year'].unique()
        
        for year in years:
            year_data = df[df['Year'] == year]
            
            # Create a basic structure for the year's data
            data[year] = {
                'ministry_allocation': pd.DataFrame({
                    'Ministry': year_data['Ministry'] if 'Ministry' in year_data.columns else ['N/A'],
                    'Allocation (in Crores)': year_data['Allocation'] if 'Allocation' in year_data.columns else [0]
                }),
                
                'budget_summary': {
                    'Total Budget': year_data['Total_Budget'].iloc[0] if 'Total_Budget' in year_data.columns else 0,
                    'Fiscal Deficit': year_data['Fiscal_Deficit'].iloc[0] if 'Fiscal_Deficit' in year_data.columns else 0,
                    'Fiscal Deficit %': year_data['Fiscal_Deficit_Percentage'].iloc[0] if 'Fiscal_Deficit_Percentage' in year_data.columns else 0,
                    'GDP': year_data['GDP'].iloc[0] if 'GDP' in year_data.columns else 0
                }
            }
    else:
        # If no year column, assume it's for a single year (current year)
        current_year = 2024
        data[current_year] = {
            'ministry_allocation': pd.DataFrame({
                'Ministry': df['Ministry'] if 'Ministry' in df.columns else ['N/A'],
                'Allocation (in Crores)': df['Allocation'] if 'Allocation' in df.columns else [0]
            }),
            
            'budget_summary': {
                'Total Budget': df['Total_Budget'].iloc[0] if 'Total_Budget' in df.columns else 0,
                'Fiscal Deficit': df['Fiscal_Deficit'].iloc[0] if 'Fiscal_Deficit' in df.columns else 0,
                'Fiscal Deficit %': df['Fiscal_Deficit_Percentage'].iloc[0] if 'Fiscal_Deficit_Percentage' in df.columns else 0,
                'GDP': df['GDP'].iloc[0] if 'GDP' in df.columns else 0
            }
        }
    
    return data

def create_bar_chart(df, x_col, y_col, title, color=None, horizontal=False):
    """Create a bar chart using Plotly"""
    if horizontal:
        fig = px.bar(df, y=x_col, x=y_col, title=title, orientation='h', color=color)
    else:
        fig = px.bar(df, x=x_col, y=y_col, title=title, color=color)
    
    fig.update_layout(
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
        legend_title_font_size=16,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_pie_chart(df, values_col, names_col, title):
    """Create a pie chart using Plotly"""
    fig = px.pie(df, values=values_col, names=names_col, title=title)
    
    fig.update_layout(
        title_font_size=20,
        legend_title_font_size=16
    )
    
    return fig

def create_donut_chart(df, values_col, names_col, title):
    """Create a donut chart using Plotly"""
    fig = px.pie(df, values=values_col, names=names_col, title=title, hole=0.4)
    
    fig.update_layout(
        title_font_size=20,
        legend_title_font_size=16
    )
    
    return fig

def create_line_chart(x, y, title, labels=None):
    """Create a line chart using Plotly"""
    if labels is None:
        labels = {"x": "X", "y": "Y"}
    
    fig = px.line(x=x, y=y, markers=True, 
                 labels=labels, title=title)
    
    fig.update_layout(
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16
    )
    
    return fig

def format_currency(amount, currency="₹"):
    """Format amount as currency with appropriate abbreviations for large numbers"""
    if amount >= 1e7:  # 10,000,000 (10 million or 1 crore)
        return f"{currency} {amount/1e7:.2f} Cr"
    elif amount >= 1e5:  # 100,000 (1 lakh)
        return f"{currency} {amount/1e5:.2f} L"
    else:
        return f"{currency} {amount:,.2f}"

def generate_insights(data, year):
    """Generate insights based on the data for a specific year"""
    insights = []
    
    try:
        year_data = data[year]
        
        # Budget allocation insights
        ministry_df = year_data['ministry_allocation']
        top_ministry = ministry_df.loc[ministry_df['Allocation (in Crores)'].idxmax()]
        insights.append(f"The {top_ministry['Ministry']} ministry has the highest allocation at {format_currency(top_ministry['Allocation (in Crores)'] * 1e7)}.")
        
        # Budget summary insights
        summary = year_data['budget_summary']
        insights.append(f"The total budget for {year} is {format_currency(summary['Total Budget'] * 1e7)}.")
        insights.append(f"The fiscal deficit is {summary['Fiscal Deficit %']}% of GDP.")
        
        # Spending type insights
        if 'spending_type' in year_data:
            spending_df = year_data['spending_type']
            capital_exp = spending_df.loc[spending_df['Type'] == 'Capital Expenditure', 'Amount (in Crores)'].iloc[0]
            revenue_exp = spending_df.loc[spending_df['Type'] == 'Revenue Expenditure', 'Amount (in Crores)'].iloc[0]
            total_exp = capital_exp + revenue_exp
            
            insights.append(f"Capital expenditure accounts for {(capital_exp/total_exp)*100:.1f}% of total expenditure.")
            insights.append(f"Revenue expenditure accounts for {(revenue_exp/total_exp)*100:.1f}% of total expenditure.")
    
    except Exception as e:
        insights.append(f"Could not generate insights due to data structure issues: {e}")
    
    return insights 