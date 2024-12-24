import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_forecast(black_bunches, bunch_weight, palms, distribution_fractions, loss_rate=0):
    """
    Calculate crop forecast using the Ulu Bernam method:
    t_n = b * w_n * p * f_n * (1-l)
    """
    forecast = []
    for n in range(3):  # Changed to 3 months
        tonnes = (black_bunches * bunch_weight * palms * distribution_fractions[n] * 
                 (1 - loss_rate)) / 1000  # Convert kg to tonnes
        forecast.append(tonnes)
    return forecast

def main():
    st.title("Ramalan Hasil Kelapa Sawit - Kiraan Tandan Hitam (BBC)")
    st.write("""
    Aplikasi ini menggunakan kaedah Ulu Bernam untuk meramal hasil kelapa sawit berdasarkan kiraan tandan hitam.
    Ramalan dibuat untuk tempoh 3 bulan akan datang.
    """)

    # Sidebar for input parameters
    st.sidebar.header("Parameter Bancian")
    
    # Block information
    total_blocks = st.sidebar.number_input("Jumlah blok", min_value=1, value=50)
    survey_block_ratio = st.sidebar.selectbox(
        "Nisbah blok dibanci (1 dalam X blok)",
        options=[5, 10],
        help="Biasanya 1 dalam 5 blok dibanci"
    )
    
    row_sampling_ratio = st.sidebar.selectbox(
        "Nisbah baris dibanci (1 dalam X baris)",
        options=[20],
        help="Biasanya baris ke-20 dibanci (5% pokok)"
    )

    # Basic block parameters
    st.header("Parameter Blok")
    col1, col2 = st.columns(2)
    
    with col1:
        palms_per_block = st.number_input("Bilangan pokok per blok", min_value=100, value=136)
        palm_age = st.number_input("Umur pokok (tahun selepas tanam)", min_value=3, value=7)
    
    with col2:
        bunch_weight = st.number_input("Purata berat tandan (kg)", min_value=1.0, value=15.0)
        loss_rate = st.number_input("Kadar kehilangan (%)", min_value=0.0, max_value=100.0, value=0.0) / 100

    # BBC Survey Data
    st.header("Data Bancian BBC")
    
    survey_blocks = total_blocks // survey_block_ratio
    rows_per_block = 30  # Standard assumption
    survey_rows = rows_per_block // row_sampling_ratio
    palms_surveyed = survey_blocks * survey_rows * (rows_per_block // row_sampling_ratio)
    
    st.write(f"Bilangan blok untuk dibanci: {survey_blocks}")
    st.write(f"Bilangan baris untuk dibanci per blok: {survey_rows}")
    st.write(f"Jumlah pokok untuk dibanci: {palms_surveyed}")

    # Anthesis bunch count data
    st.header("Kiraan Tandan Selepas Pendebungaan")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bunch_3_month = st.number_input("Jumlah tandan (3 bulan selepas pendebungaan)", min_value=0, value=0)
    with col2:
        bunch_4_month = st.number_input("Jumlah tandan (4 bulan selepas pendebungaan)", min_value=0, value=0)
    with col3:
        bunch_5_month = st.number_input("Jumlah tandan (5 bulan selepas pendebungaan)", min_value=0, value=0)

    # Black bunch count
    st.header("Kiraan Tandan Hitam")
    black_bunches = st.number_input("Jumlah tandan hitam", min_value=0, value=100)
    
    if black_bunches > 0:
        bunches_per_palm = black_bunches / palms_surveyed
        st.write(f"Purata tandan hitam per pokok: {bunches_per_palm:.2f}")
    
    # Distribution fractions
    st.header("Agihan Bulanan")
    st.write("Masukkan jangkaan agihan kemasakan tandan untuk 3 bulan akan datang (jumlah mesti 1.0)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        month1_dist = st.number_input("Bulan 1", min_value=0.0, max_value=1.0, value=0.4)
    with col2:
        month2_dist = st.number_input("Bulan 2", min_value=0.0, max_value=1.0, value=0.35)
    with col3:
        month3_dist = st.number_input("Bulan 3", min_value=0.0, max_value=1.0, value=0.25)
    
    distribution_sum = month1_dist + month2_dist + month3_dist
    if abs(distribution_sum - 1.0) > 0.001:
        st.warning(f"Jumlah agihan adalah {distribution_sum:.2f}. Ia perlu berjumlah 1.0")
    
    distribution_fractions = [month1_dist, month2_dist, month3_dist]
    
    # Calculate forecast
    if st.button("Kira Ramalan"):
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
            st.header("Keputusan Ramalan")
            
            # Create forecast dates
            current_date = datetime.now()
            dates = [(current_date + timedelta(days=30*i)).strftime('%B %Y') for i in range(1, 4)]
            
            # Create forecast dataframe
            forecast_df = pd.DataFrame({
                'Bulan': dates,
                'Jangkaan Pengeluaran (tan)': forecast,
                'Agihan (%)': [d*100 for d in distribution_fractions]
            })
            
            st.dataframe(forecast_df.style.format({
                'Jangkaan Pengeluaran (tan)': '{:.1f}',
                'Agihan (%)': '{:.1f}%'
            }))
            
            # Total forecast
            st.write(f"Jumlah ramalan 3 bulan: {sum(forecast):.1f} tan")
            
            # Create a simple bar chart
            st.bar_chart(data=pd.DataFrame({
                'Bulan': dates,
                'Tan': forecast
            }).set_index('Bulan'))

            # Display anthesis bunch counts summary
            st.header("Ringkasan Kiraan Tandan Selepas Pendebungaan")
            anthesis_df = pd.DataFrame({
                'Tempoh': ['3 Bulan', '4 Bulan', '5 Bulan'],
                'Jumlah Tandan': [bunch_3_month, bunch_4_month, bunch_5_month]
            })
            st.dataframe(anthesis_df)

if __name__ == "__main__":
    main()
