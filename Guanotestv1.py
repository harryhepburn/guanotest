import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_survey_requirements(total_area):
    """Calculate 5% survey area requirements"""
    survey_area = total_area * 0.05
    return survey_area

def calculate_theoretical_trees(area, trees_per_ha):
    """Calculate theoretical number of trees based on area and density"""
    return area * trees_per_ha

def calculate_bunch_distribution(bunch_3_month, bunch_4_month, bunch_5_month, total_trees_surveyed):
    """Calculate bunch distribution and averages"""
    total_bunches = bunch_3_month + bunch_4_month + bunch_5_month
    if total_bunches == 0 or total_trees_surveyed == 0:
        return {
            'distribution': [0, 0, 0],
            'avg_bunches_per_tree': 0,
            'percentages': [0, 0, 0]
        }
    
    # Calculate percentages
    percentages = [
        bunch_5_month / total_bunches,  # Will mature next month
        bunch_4_month / total_bunches,  # Will mature in 2 months
        bunch_3_month / total_bunches   # Will mature in 3 months
    ]
    
    # Calculate average bunches per tree
    avg_bunches = total_bunches / total_trees_surveyed
    
    return {
        'distribution': percentages,
        'avg_bunches_per_tree': avg_bunches,
        'percentages': [bunch_5_month, bunch_4_month, bunch_3_month]
    }

def get_forecast_months():
    """Get the next three months starting from next month"""
    current_date = datetime.now()
    # Start from the first day of next month
    if current_date.month == 12:
        next_month = datetime(current_date.year + 1, 1, 1)
    else:
        next_month = datetime(current_date.year, current_date.month + 1, 1)
    
    months = []
    for i in range(3):
        month_date = next_month + timedelta(days=32*i)
        # Ensure we're getting the first day of each month
        month_date = month_date.replace(day=1)
        months.append(month_date.strftime('%B %Y'))
    return months

def main():
    st.title("Ramalan Hasil Kelapa Sawit - Kiraan Tandan Hitam (BBC)")
    st.write("""
    Sistem ramalan hasil berdasarkan kiraan tandan hitam dan bancian tandan selepas pendebungaan.
    """)

    # Step 1: Basic Plantation Information
    st.header("1. Maklumat Asas Ladang")
    col1, col2 = st.columns(2)
    with col1:
        total_area = st.number_input("Jumlah Keluasan Ladang (Hektar)", min_value=1.0, value=100.0)
        trees_per_ha = st.number_input("Bilangan Pokok Per Hektar", min_value=100, value=136)
    with col2:
        bunch_weight = st.number_input("Purata Berat Tandan (kg)", min_value=1.0, value=15.0)
        loss_rate = st.number_input("Kadar Kehilangan (%)", min_value=0.0, max_value=100.0, value=0.0) / 100

    # Calculate and display survey requirements
    survey_area = calculate_survey_requirements(total_area)
    theoretical_total_trees = calculate_theoretical_trees(total_area, trees_per_ha)
    theoretical_survey_trees = calculate_theoretical_trees(survey_area, trees_per_ha)

    st.header("2. Maklumat Kawasan Bancian")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Keluasan kawasan bancian (5%): {survey_area:.2f} hektar")
        st.write(f"Anggaran bilangan pokok dalam kawasan bancian: {theoretical_survey_trees:.0f}")
    
    # Step 2: Actual Survey Data
    with col2:
        actual_surveyed_trees = st.number_input("Bilangan sebenar pokok dibanci", 
                                              min_value=1, 
                                              value=int(theoretical_survey_trees))
    
    # Calculate and show variance
    tree_variance = ((actual_surveyed_trees - theoretical_survey_trees) / theoretical_survey_trees) * 100
    st.write(f"Varians bilangan pokok: {tree_variance:.1f}%")

    # Step 3: Bunch Count Data
    st.header("3. Kiraan Tandan Selepas Pendebungaan")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bunch_3_month = st.number_input("3 bulan selepas pendebungaan", min_value=0, value=0)
    with col2:
        bunch_4_month = st.number_input("4 bulan selepas pendebungaan", min_value=0, value=0)
    with col3:
        bunch_5_month = st.number_input("5 bulan selepas pendebungaan", min_value=0, value=0)

    # Calculate distributions and averages
    bunch_stats = calculate_bunch_distribution(
        bunch_3_month, bunch_4_month, bunch_5_month, actual_surveyed_trees
    )

    # Get forecast months
    forecast_months = get_forecast_months()

    # Display bunch statistics
    st.header("4. Analisis Bancian")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Taburan Tandan")
        bunch_df = pd.DataFrame({
            'Peringkat': [
                f'5 Bulan ({forecast_months[0]})', 
                f'4 Bulan ({forecast_months[1]})', 
                f'3 Bulan ({forecast_months[2]})'
            ],
            'Jumlah Tandan': [bunch_5_month, bunch_4_month, bunch_3_month],
            'Peratusan (%)': [f"{x*100:.1f}%" for x in bunch_stats['distribution']]
        })
        st.dataframe(bunch_df)

    with col2:
        st.subheader("Purata Tandan Per Pokok")
        st.write(f"Purata tandan per pokok: {bunch_stats['avg_bunches_per_tree']:.2f}")

    # Calculate projected yield
    if st.button("Kira Ramalan Hasil"):
        st.header("5. Ramalan Hasil")
        
        # Calculate total projected bunches for whole plantation
        total_projected_bunches = bunch_stats['avg_bunches_per_tree'] * theoretical_total_trees
        
        # Calculate monthly projections
        monthly_projections = []
        
        for i, (month, dist) in enumerate(zip(forecast_months, bunch_stats['distribution'])):
            month_bunches = total_projected_bunches * dist
            month_tonnes = (month_bunches * bunch_weight * (1 - loss_rate)) / 1000
            
            monthly_projections.append({
                'Bulan': month,
                'Anggaran Tandan': int(month_bunches),
                'Anggaran Hasil (Tan)': month_tonnes
            })

        # Display projections
        projection_df = pd.DataFrame(monthly_projections)
        st.dataframe(projection_df.style.format({
            'Anggaran Hasil (Tan)': '{:.1f}'
        }))

        # Total projection
        total_tonnes = sum(p['Anggaran Hasil (Tan)'] for p in monthly_projections)
        st.write(f"Jumlah ramalan hasil 3 bulan: {total_tonnes:.1f} tan")
        
        # Create visualization
        st.bar_chart(data=pd.DataFrame({
            'Bulan': [p['Bulan'] for p in monthly_projections],
            'Tan': [p['Anggaran Hasil (Tan)'] for p in monthly_projections]
        }).set_index('Bulan'))



    # Add BBC Guidelines in Sidebar
    st.sidebar.header("Panduan Bancian BBC")
    
    # Schedule information
    st.sidebar.subheader("Jadual Bancian")
    schedule_data = {
        'Pusingan': [1, 2, 3, 4],
        'Bulan Dijalankan': ['Disember', 'Mac', 'Jun', 'September'],
        'Anggaran Hasil': ['Jan - Mac', 'April - Jun', 'Julai - September', 'Oktober - Disember']
    }
    st.sidebar.dataframe(pd.DataFrame(schedule_data))
    
    st.sidebar.markdown("""
    #### Panduan Umum
    1. Bancian dijalankan 4 kali setahun
    2. Luas kawasan bancian: 5% daripada jumlah kawasan
    3. Baris bancian bermula dari baris #3 dari tepi sempadan/jalan
    
    #### Panduan Bancian Tandan
    1. Kira tandan pada bulan ke-3 dan ke atas selepas pendebungaan
    2. Tandan berkilat biasanya dilihat pada pelepah 24-25
    
    #### Klasifikasi Tandan Selepas Anthesis
    """)
    
    # Create classification table
    classification_data = {
        'Bulan': ['1', '2', '3*', '4*', '5*'],
        'Kedudukan': ['20-21', '22-23', '24-25', '26-27', '28-29'],
        'Warna': ['Hijau ke Hitam', 'Hitam', 'Hitam', 'Hitam ke Merah', 'Merah ke Oren'],
        'Selaput': ['25%', '50%', '80%', '90%', '95%'],
        'Bulan Dijangka': ['5 Bulan', '4 Bulan', '3 Bulan', '2 Bulan', '1 Bulan']
    }
    
    st.sidebar.dataframe(pd.DataFrame(classification_data))
    
    st.sidebar.markdown("""
    *Tandan yang diambilkira dalam bancian
    
    #### Nota Penting
    - Pemerhatian tandan hitam bermula pada pelepah 24-25
    - Peratus selaput terbuka menunjukkan kematangan tandan
    - Ramalan hasil berdasarkan tandan yang ditemui pada peringkat 3-5 bulan selepas pendebungaan
    """)

if __name__ == "__main__":
    main()


