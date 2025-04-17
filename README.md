# Budget-Visualization

An interactive visualization tool for exploring Indian Union Budget data.

## Overview

Wallet of India is a web application that simplifies and visualizes the Indian Union Budget data in an intuitive, interactive format. The application provides multiple views to analyze budget trends, allocations, and comparisons across different years.

## Features

- **Three Main Views:**
  - **This Year:** Detailed analysis of the current year's budget
  - **Last 2 Years:** Comparison between the current and previous year's budget
  - **Last 3 Years:** Trend analysis across three years

- **Interactive Visualizations:**
  - Bar charts, pie charts, line charts, and donut charts
  - Ministry-wise allocations
  - Sector-wise expenditure
  - Revenue sources
  - Capital vs Revenue spending

- **Data Upload:**
  - Upload your own CSV or Excel file with budget data
  - Use sample data for demonstration

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd Wallet_of_India
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to: `http://localhost:8501`

3. Use the sidebar to navigate between different views and upload your own data if desired.

## Data Format

If you want to upload your own data, ensure it follows this structure:

- CSV or Excel file with columns for:
  - Year (if providing multi-year data)
  - Ministry (for ministry allocations)
  - Allocation (budget allocated to each ministry)
  - Other relevant budget metrics

## Sample Data

The application comes with sample data for demonstration purposes, which can be enabled using the "Use Sample Data" checkbox in the sidebar.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
