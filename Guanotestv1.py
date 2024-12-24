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
    for n in range(3):
        tonnes = (black_bunches * bunch_weight * palms * distribution_fractions[n] * 
                 (1 - loss_rate)) / 1000  # Convert kg to tonnes
        forecast.append(tonnes)
    return forecast

def calculate_distribution(bunch_3_month, bunch_4_month, bunch_5_month):
    """
    Calculate distribution fractions based on bunch counts after anthesis
    """
    total_bunches = bunch_3_month + bunch_4_month + bunch_5_month
    if total_bunches == 0:
        return [0.4, 0.35, 0.25]  # Default distribution if no data
    
    return [
        bunch_5_month / total_bunches,
        bunch_4_month / total_bunches,
        bunch_3_month / total_bunches
    ]

def main():
    st.title("Ramalan Hasil Kelapa Sawit - Kiraan Tandan Hitam (BBC)")
    st.write("""
    Aplikasi ini membantu pengguna meramal hasil kelapa sawit berdasarkan kiraan tandan hitam.
    Ramalan dibuat untuk tempoh 3 bulan akan datang.
    """)

    # Estate Area Information
    st.header("Maklumat Kawasan Ladang")
    estate_area = st.number_input("Keluasan Ladang (Hektar)", min_value=1.0, value=100.0)
    
    # Calculate 5% survey area
    survey_area = estate_area * 0.05
    st.write(f"Keluasan kawasan bancian (5%): {survey_area:.2f} hektar")

    # Block information
    st.header("Maklumat Blok")
    total_blocks = st.number_input("Jumlah blok", min_value=1, value=50)
    palms_per_block = st.number_input("Bilangan pokok per blok", min_value=100, value=136)
    palm_age = st.number_input("Umur pokok (tahun selepas tanam)", min_value=3, value=7)
    
    # Calculate area per block
    area_per_block = estate_area / total_blocks
    st.write(f"Keluasan per blok: {area_per_block:.2f} hektar")
    
    # Calculate number of blocks to survey (5%)
    blocks_to_survey = max(1, round(total_blocks * 0.05))
    st.write(f"Bilangan blok untuk dibanci (5%): {blocks_to_survey}")

    # Basic parameters
    st.header("Parameter Asas")
    col1, col2 = st.columns(2)
    
    with col1:
        bunch_weight = st.number_input("Purata berat tandan (kg)", min_value=1.0, value=15.0)
    with col2:
        loss_rate = st.number_input("Kadar kehilangan (%)", min_value=0.0, max_value=100.0, value=0.0) / 100

    # Anthesis bunch count data
    st.header("Kiraan Tandan Selepas Pendebungaan")
    st.write("Masukkan bilangan tandan yang ditemui pada peringkat berikut:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bunch_3_month = st.number_input("3 bulan selepas pendebungaan", min_value=0, value=0)
    with col2:
        bunch_4_month = st.number_input("4 bulan selepas pendebungaan", min_value=0, value=0)
    with col3:
        bunch_5_month = st.number_input("5 bulan selepas pendebungaan", min_value=0, value=0)

    # Calculate distribution automatically
    distribution_fractions = calculate_distribution(bunch_3_month, bunch_4_month, bunch_5_month)

    # Display calculated distribution
    st.header("Agihan Bulanan (Dikira Automatik)")
    dist_df = pd.DataFrame({
        'Bulan': ['Bulan 1', 'Bulan 2', 'Bulan 3'],
        'Agihan (%)': [f'{d*100:.1f}%' for d in distribution_fractions]
    })
    st.dataframe(dist_df)

    # Black bunch count
    st.header("Kiraan Tandan Hitam (BBC)")
    black_bunches = st.number_input("Jumlah tandan hitam dalam kawasan bancian", min_value=0, value=100)
    
    if black_bunches > 0:
        # Calculate bunches per hectare instead of per palm
        bunches_per_hectare = black_bunches / survey_area
        st.write(f"Purata tandan hitam per hektar: {bunches_per_hectare:.2f}")
    
    # Calculate forecast
    if st.button("Kira Ramalan"):
        if black_bunches > 0:
            total_palms = total_blocks * palms_per_block
            bunches_per_palm = black_bunches / (blocks_to_survey * palms_per_block)
            
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
            st.header("Ringkasan Kiraan Tandan")
            anthesis_df = pd.DataFrame({
                'Peringkat': ['3 Bulan Selepas Pendebungaan', '4 Bulan Selepas Pendebungaan', '5 Bulan Selepas Pendebungaan'],
                'Jumlah Tandan': [bunch_3_month, bunch_4_month, bunch_5_month],
                'Peratusan': [f'{(x/sum([bunch_3_month, bunch_4_month, bunch_5_month])*100):.1f}%' if sum([bunch_3_month, bunch_4_month, bunch_5_month]) > 0 else '0.0%' 
                             for x in [bunch_3_month, bunch_4_month, bunch_5_month]]
            })
            st.dataframe(anthesis_df)

if __name__ == "__main__":
    main()
