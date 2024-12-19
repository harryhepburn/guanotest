import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_forecast(black_bunches, bunch_weight, palms, distribution_fractions, loss_rate=0):
    """
    Calculate crop forecast using the Ulu Bernam method:
    t_n = b * w_n * p * f_n * (1-l)
    where:
    t_n = output in tonnes in month n after black bunch count
    b = black bunches per palm
    w_n = expected bunch weight in month n
    p = number of palms
    f_n = fraction expected to be ripe in month n
    l = loss factor
    """
    forecast = []
    for n in range(4):
        tonnes = (black_bunches * bunch_weight * palms * distribution_fractions[n] * 
                 (1 - loss_rate)) / 1000  # Convert kg to tonnes
        forecast.append(tonnes)
    return forecast

def main():
    st.title("Oil Palm Black Bunch Count (BBC) Forecast")
    st.write("""
    This application implements the Ulu Bernam method for crop forecasting based on black bunch counts.
    It provides a 4-month forecast of expected oil palm production.
    """)

    # Sidebar for input parameters
    st.sidebar.header("Survey Parameters")
    
    # Block information
    total_blocks = st.sidebar.number_input("Total number of blocks", min_value=1, value=50)
    survey_block_ratio = st.sidebar.selectbox(
        "Survey block ratio (1 in X blocks)",
        options=[5, 10],
        help="Typically 1 in 5 blocks are surveyed"
    )
    
    row_sampling_ratio = st.sidebar.selectbox(
        "Row sampling ratio (1 in X rows)",
        options=[20],
        help="Typically every 20th row is surveyed (5% of palms)"
    )

    # Basic block parameters
    st.header("Block Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        palms_per_block = st.number_input("Palms per block", min_value=100, value=136)
        palm_age = st.number_input("Palm age (years after planting)", min_value=3, value=7)
    
    with col2:
        bunch_weight = st.number_input("Average bunch weight (kg)", min_value=1.0, value=15.0)
        loss_rate = st.number_input("Loss rate (%)", min_value=0.0, max_value=100.0, value=0.0) / 100

    # BBC Survey Data
    st.header("BBC Survey Data")
    
    survey_blocks = total_blocks // survey_block_ratio
    rows_per_block = 30  # Standard assumption
    survey_rows = rows_per_block // row_sampling_ratio
    palms_surveyed = survey_blocks * survey_rows * (rows_per_block // row_sampling_ratio)
    
    st.write(f"Number of blocks to survey: {survey_blocks}")
    st.write(f"Number of rows to survey per block: {survey_rows}")
    st.write(f"Total palms to be surveyed: {palms_surveyed}")
    
    black_bunches = st.number_input("Total black bunches counted", min_value=0, value=100)
    
    if black_bunches > 0:
        bunches_per_palm = black_bunches / palms_surveyed
        st.write(f"Average black bunches per palm: {bunches_per_palm:.2f}")
    
    # Distribution fractions
    st.header("Monthly Distribution")
    st.write("Enter the expected distribution of bunch ripening over the next 4 months (must sum to 1.0)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        month1_dist = st.number_input("Month 1", min_value=0.0, max_value=1.0, value=0.3)
    with col2:
        month2_dist = st.number_input("Month 2", min_value=0.0, max_value=1.0, value=0.3)
    with col3:
        month3_dist = st.number_input("Month 3", min_value=0.0, max_value=1.0, value=0.25)
    with col4:
        month4_dist = st.number_input("Month 4", min_value=0.0, max_value=1.0, value=0.15)
    
    distribution_sum = month1_dist + month2_dist + month3_dist + month4_dist
    if abs(distribution_sum - 1.0) > 0.001:
        st.warning(f"Distribution fractions sum to {distribution_sum:.2f}. They should sum to 1.0")
    
    distribution_fractions = [month1_dist, month2_dist, month3_dist, month4_dist]
    
    # Calculate forecast
    if st.button("Calculate Forecast"):
        if black_bunches > 0:
            total_palms = total_blocks * palms_per_block
            bunches_per_palm = black_bunches / palms_surveyed
            
            # Calculate forecast
            forecast = calculate_forecast(
                bunches_per_palm,
                bunch_weight,
                total_palms,
                distribution_fractions,
                loss_rate
            )
            
            # Display results
            st.header("Forecast Results")
            
            # Create forecast dates
            current_date = datetime.now()
            dates = [(current_date + timedelta(days=30*i)).strftime('%B %Y') for i in range(1, 5)]
            
            # Create forecast dataframe
            forecast_df = pd.DataFrame({
                'Month': dates,
                'Expected Production (tonnes)': forecast,
                'Distribution (%)': [d*100 for d in distribution_fractions]
            })
            
            st.dataframe(forecast_df.style.format({
                'Expected Production (tonnes)': '{:.1f}',
                'Distribution (%)': '{:.1f}%'
            }))
            
            # Total forecast
            st.write(f"Total 4-month forecast: {sum(forecast):.1f} tonnes")
            
            # Create a simple bar chart
            st.bar_chart(data=pd.DataFrame({
                'Month': dates,
                'Tonnes': forecast
            }).set_index('Month'))

if __name__ == "__main__":
    main()
