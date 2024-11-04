import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
from datetime import datetime

def calculate_weather_factor():
    # Get current month for seasonal adjustment
    current_month = datetime.now().month
    # Monsoon season adjustment (adjust these months according to your location)
    monsoon_months = [11, 12, 1, 2]  # Example monsoon months
    if current_month in monsoon_months:
        return 0.7  # Higher spread rate during monsoon
    return 0.5

def calculate_age_factor(tahuntuai):
    # Age-based susceptibility factor
    if tahuntuai < 5:
        return 0.3  # Young palms are less susceptible
    elif tahuntuai < 10:
        return 0.5  # Mid-age palms
    else:
        return 0.7  # Older palms are more susceptible

def calculate_infection_pressure(total_palms, infected_palms):
    # Calculate infection pressure based on current infection density
    infection_ratio = infected_palms / total_palms if total_palms > 0 else 0
    return min(0.8, infection_ratio * 1.2)  # Cap at 80% maximum pressure

def predict_disease_progression(hasilsemasa, tahuntuai, total_palms, infected_palms, years, is_controlled=True):
    weather_factor = calculate_weather_factor()
    age_factor = calculate_age_factor(tahuntuai)
    infection_pressure = calculate_infection_pressure(total_palms, infected_palms)
    
    # Base reduction rates
    if is_controlled:
        base_reduction = 0.1 * (1 + weather_factor) * age_factor * infection_pressure
    else:
        base_reduction = 0.6 * (1 + weather_factor) * age_factor * infection_pressure
    
    # Calculate yearly yields with dynamic reduction
    yields = [hasilsemasa]
    current_yield = hasilsemasa
    
    for year in range(len(years)):
        # Adjust reduction rate based on cumulative effect
        cumulative_factor = 1 + (year * 0.05)  # Increases impact over time
        adjusted_reduction = min(0.9, base_reduction * cumulative_factor)  # Cap at 90% reduction
        
        current_yield *= (1 - adjusted_reduction)
        yields.append(max(current_yield, hasilsemasa * 0.1))  # Ensure yield doesn't go below 10% of initial
    
    return yields[1:]  # Remove initial yield

def main():
    st.set_page_config(page_title="GUANO Calculator", page_icon="🌴", layout="wide")
    
    # [Previous code remains the same until the prediction section]
    
    st.write("---")
    st.subheader("Anggaran Hasil")

    total_palms = serangan_a + serangan_b + serangan_c + serangan_d + serangan_e + serangan_f
    infected_palms = serangan_a + serangan_b + serangan_c + serangan_d + serangan_f

    hasilsemasa = (0.1 * serangan_a) + (0.1 * serangan_d) + (0.18 * serangan_e) + (0.15 * serangan_f)
    st.metric("Hasil Semasa", f"{hasilsemasa:.2f} MT/Tahun")

    # Weather condition input
    st.write("### Faktor Cuaca dan Persekitaran")
    rainfall = st.slider("Purata Hujan Bulanan (mm)", 0, 500, 250)
    soil_condition = st.selectbox("Keadaan Tanah", 
                                ["Sangat Baik", "Baik", "Sederhana", "Kurang Baik"],
                                index=1)

    tahuntuai1 = tahuntuai + 1
    years = list(range(tahuntuai1, 26))

    # Calculate yields with improved prediction model
    dirawat_yields = predict_disease_progression(
        hasilsemasa, tahuntuai, total_palms, infected_palms, 
        years, is_controlled=True
    )
    
    dibiar_yields = predict_disease_progression(
        hasilsemasa, tahuntuai, total_palms, infected_palms, 
        years, is_controlled=False
    )

    # Create DataFrame for display
    df = pd.DataFrame({
        'Tahun': years,
        'Kawalan (MT)': [round(y, 2) for y in dirawat_yields],
        'Tiada Kawalan (MT)': [round(y, 2) for y in dibiar_yields]
    })

    st.write(df)
    st.write('''
    Nota: Anggaran pengurangan hasil berdasarkan:
    - Tekanan jangkitan semasa
    - Umur pokok
    - Keadaan cuaca
    - Faktor persekitaran
    - Kepadatan jangkitan
    ''')

    # Enhanced visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Line plot
    ax1.plot(years, dirawat_yields, label='Kawalan', color='green', marker='o')
    ax1.plot(years, dibiar_yields, label='Tiada Kawalan', color='red', marker='o')
    ax1.set_xlabel('Tahun')
    ax1.set_ylabel('Hasil (MT)')
    ax1.set_title('Perbandingan Hasil Antara Kawalan dan Tiada Kawalan')
    ax1.legend()
    ax1.grid(True)

    # Bar plot showing yearly reduction
    yearly_reduction_control = [abs(dirawat_yields[i] - dirawat_yields[i-1]) 
                              for i in range(1, len(dirawat_yields))]
    yearly_reduction_no_control = [abs(dibiar_yields[i] - dibiar_yields[i-1]) 
                                 for i in range(1, len(dibiar_yields))]
    
    x = years[1:]
    width = 0.35
    ax2.bar([x - width/2 for x in x], yearly_reduction_control, width, 
            label='Kawalan', color='green', alpha=0.6)
    ax2.bar([x + width/2 for x in x], yearly_reduction_no_control, width, 
            label='Tiada Kawalan', color='red', alpha=0.6)
    ax2.set_xlabel('Tahun')
    ax2.set_ylabel('Pengurangan Hasil (MT)')
    ax2.set_title('Pengurangan Hasil Tahunan')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    st.pyplot(fig)

    # [Rest of the code remains the same]

if __name__ == "__main__":
    main()
