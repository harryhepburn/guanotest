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
        bunch_5_month / total_bunches,  # Will mature in 1 month
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

    # Display bunch statistics
    st.header("4. Analisis Bancian")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Taburan Tandan")
        bunch_df = pd.DataFrame({
            'Peringkat': ['5 Bulan (Bulan 1)', '4 Bulan (Bulan 2)', '3 Bulan (Bulan 3)'],
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
        current_date = datetime.now()
        
        for i, dist in enumerate(bunch_stats['distribution']):
            month_date = (current_date + timedelta(days=30*i)).strftime('%B %Y')
            month_bunches = total_projected_bunches * dist
            month_tonnes = (month_bunches * bunch_weight * (1 - loss_rate)) / 1000
            
            monthly_projections.append({
                'Bulan': month_date,
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

if __name__ == "__main__":
    main()
