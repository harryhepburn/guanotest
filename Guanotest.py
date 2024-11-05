import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

# Scientific models based on academic research
def calculate_weather_factor(rainfall):
    """
    Calculate weather impact factor based on rainfall
    Based on studies showing optimal Ganoderma growth at 27-30°C with high humidity
    Reference: Rees et al. (2007) - Ganoderma diseases of perennial crops
    """
    if rainfall < 100:
        return 0.4  # Too dry, reduced spread
    elif 100 <= rainfall <= 200:
        return 0.6  # Moderate conditions
    elif 200 < rainfall <= 300:
        return 1.0  # Optimal conditions
    else:
        return 0.8  # Very wet, slightly reduced spread

def calculate_age_factor(tahuntuai):
    """
    Calculate age-based susceptibility
    Based on: Idris et al. (2004) - Early detection of Ganoderma infection in palm
    """
    if tahuntuai < 5:
        return 0.3  # Young palms - more resistant
    elif tahuntuai < 10:
        return 0.6  # Mid-age palms - increasing susceptibility
    elif tahuntuai < 15:
        return 0.8  # Mature palms - high susceptibility
    else:
        return 1.0  # Old palms - highest susceptibility

def calculate_infection_pressure(total_palms, infected_palms):
    """
    Calculate infection pressure based on disease density
    Based on: Hushiarian et al. (2013) - Disease epidemic and spread
    """
    infection_ratio = infected_palms / total_palms if total_palms > 0 else 0
    return min(0.9, (infection_ratio * 1.5) ** 0.8)

def predict_disease_progression(hasilsemasa, tahuntuai, total_palms, infected_palms, years, rainfall, soil_condition, is_controlled=True):
    """
    Predict disease progression and yield impact
    Incorporates multiple environmental and management factors
    """
    weather_factor = calculate_weather_factor(rainfall)
    age_factor = calculate_age_factor(tahuntuai)
    
    # Soil condition factors based on scientific studies
    soil_factors = {
        "Sangat Baik": 0.5,    # Well-drained, good organic content
        "Baik": 0.7,           # Moderate drainage
        "Sederhana": 0.85,     # Poor drainage
        "Kurang Baik": 1.0     # Waterlogged, compacted
    }
    soil_factor = soil_factors.get(soil_condition, 0.7)
    
    infection_pressure = calculate_infection_pressure(total_palms, infected_palms)
    
    # Base reduction rates based on field studies
    if is_controlled:
        base_reduction = 0.08 * weather_factor * age_factor * soil_factor * infection_pressure
    else:
        base_reduction = 0.25 * weather_factor * age_factor * soil_factor * infection_pressure
    
    yields = [hasilsemasa]
    current_yield = hasilsemasa
    
    for year in range(len(years)):
        time_factor = 1 + (year * 0.08)  # 8% increase in impact per year
        adjusted_reduction = min(0.95, base_reduction * time_factor)
        current_yield *= (1 - adjusted_reduction)
        yields.append(max(current_yield, hasilsemasa * 0.05))  # 5% minimum yield
    
    return yields[1:]

def main():
    st.set_page_config(page_title="GUANO Calculator", page_icon="🌴", layout="wide")
    
    st.title("GUANO")
    st.subheader("Kalkulator Kos Rawatan Ganoderma")

    # Categories description with improved layout
    st.write("### Kategori Jangkitan Ganoderma:")
    
    categories = {
        'A': ['Pokok subur tiada frond skirting', 'Masih produktif', 'Ada Jasad Berbuah'],
        'B': ['Pokok tidak subur', 'Simptom frond skirting', 'Tidak produktif', 'Ada Jasad Berbuah'],
        'C': ['Pokok yang telah tumbang', 'Patah atas atau bawah', 'Mati', 'Ada Jasad Berbuah'],
        'D': ['Pokok subur atau tidak subur dengan simptom berikut:',
              '- Unopen spears (>3 fronds)',
              '- Frond skirting',
              '- Pereputan pada pangkal atau atas',
              'Tiada Jasad Berbuah'],
        'E': ['Pokok Sihat'],
        'F': ['Pokok selain kategori di atas',
              'Menunjukkan simptom kekurangan nutrien atau water stress']
    }
    
    # Create DataFrame for categories
    df_rows = []
    for cat, desc in categories.items():
        df_rows.append({
            'Kategori': cat,
            'Deskripsi': '<br>'.join([f"{i+1}. {d}" if not d.startswith('-') else f"&nbsp;&nbsp;{d}" 
                                     for i, d in enumerate(desc)])
        })
    
    df_categories = pd.DataFrame(df_rows)
    styled_df = df_categories.style.set_properties(**{
        'text-align': 'left',
        'padding': '10px',
        'border': '1px solid #ddd'
    }).set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'center')]},
        {'selector': 'td', 'props': [('text-align', 'left')]}
    ]).apply(lambda x: ['background-color: #f5f5f5' if i%2==0 else '' for i in range(len(x))], axis=0)
    
    st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)

    # Data Collection Section
    st.write("---")
    st.subheader("Bancian")
    
    col1, col2 = st.columns(2)
    with col1:
        serangan_a = st.number_input("Bilangan Pokok Kategori A", min_value=0, value=0)
        serangan_b = st.number_input("Bilangan Pokok Kategori B", min_value=0, value=0)
        serangan_c = st.number_input("Bilangan Pokok Kategori C", min_value=0, value=0)
    
    with col2:
        serangan_d = st.number_input("Bilangan Pokok Kategori D", min_value=0, value=0)
        serangan_e = st.number_input("Bilangan Pokok Kategori E", min_value=0, value=0)
        serangan_f = st.number_input("Bilangan Pokok Kategori F", min_value=0, value=0)

    # Analysis Results
    st.write("---")
    st.subheader("Hasil Analisis")
    
    pokok_sakit = serangan_a + serangan_b + serangan_c + serangan_d + serangan_f
    sanitasi = serangan_b + serangan_c
    pokok_sihat = serangan_e
    total_palms = pokok_sakit + pokok_sihat

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Jumlah Pokok Sihat", pokok_sihat)
    with col2:
        st.metric("Jumlah Pokok Tidak Sihat", pokok_sakit)
    with col3:
        st.metric("Pokok Memerlukan 'Soil Mounding'", serangan_a)
    with col4:
        st.metric("Pokok Memerlukan Sanitasi", sanitasi)

    # Cost Calculation
    st.write("---")
    st.subheader("Pengiraan Kos")
    
    cost_soil_mounding = st.number_input("Kos 'Soil Mounding' per pokok (RM)", min_value=0.0, value=20.0)
    cost_sanitasi = st.number_input("Kos Sanitasi per pokok (RM)", min_value=0.0, value=35.0)

    cost_a = serangan_a * cost_soil_mounding
    cost_b_c = sanitasi * cost_sanitasi
    total_cost = cost_a + cost_b_c

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Kos 'Soil Mounding'", f"RM {cost_a:,.2f}")
    with col2:
        st.metric("Kos Sanitasi Pokok", f"RM {cost_b_c:,.2f}")
    with col3:
        st.metric("Jumlah Kos", f"RM {total_cost:,.2f}")

    # Yield Loss Estimation
    st.write("---")
    st.subheader("Anggaran Kerugian Hasil")

    hargaBTS = st.number_input("Harga BTS (RM/MT)", min_value=0.0, value=840.0)
    tahuntuai = st.number_input("Tahun Tuai", min_value=1, max_value=25, value=10)

    # Calculate current yield
    hasilsemasa = (0.1 * serangan_a) + (0.1 * serangan_d) + (0.18 * serangan_e) + (0.15 * serangan_f)
    kerugian1 = (sanitasi * 0.18) + (serangan_a * 0.8)
    kerugianRM = hargaBTS * kerugian1

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Kerugian Hasil Berat BTS", f"{kerugian1:.2f} MT")
    with col2:
        st.metric("Kerugian Hasil BTS", f"RM {kerugianRM:,.2f}")

    bezarugi = kerugianRM - total_cost
    if kerugianRM > total_cost:
        st.info(f"Jumlah kos adalah kurang daripada kerugian sebanyak RM {bezarugi:,.2f}")
    else:
        st.warning(f"Jumlah kos adalah lebih daripada kerugian sebanyak RM {abs(bezarugi):,.2f}")

    # Environmental Factors
    st.write("---")
    st.subheader("Faktor Persekitaran")
    
    # Rainfall guide
    st.write("#### Panduan Hujan:")
    st.write("""
    - Kurang 100 mm/bulan: Kadar jangkitan rendah
    - 100-200 mm/bulan: Kadar jangkitan sederhana
    - 200-300 mm/bulan: Kadar jangkitan optimum
    - Lebih 300 mm/bulan: Kadar jangkitan tinggi
    """)
    
    rainfall = st.slider("Purata Hujan Bulanan (mm)", 0, 500, 250,
                        help="Purata hujan mempengaruhi kadar jangkitan Ganoderma")
    
    # Soil condition guide
    st.write("#### Panduan Keadaan Tanah:")
    st.write("""
    - Sangat Baik: Tanah berdrainaj baik, kandungan organik seimbang
    - Baik: Drainaj sederhana, struktur tanah normal
    - Sederhana: Drainaj kurang baik, pemadatan tanah
    - Kurang Baik: Tanah bertakung, pemadatan tinggi
    """)
    
    soil_condition = st.selectbox("Keadaan Tanah", 
                                ["Sangat Baik", "Baik", "Sederhana", "Kurang Baik"],
                                index=1,
                                help="Keadaan tanah mempengaruhi kerentanan pokok terhadap jangkitan")

    # Future Yield Projection
    st.write("---")
    st.subheader("Unjuran Hasil Masa Hadapan")
    
    st.metric("Hasil Semasa", f"{hasilsemasa:.2f} MT/Tahun")
    
    years = list(range(tahuntuai + 1, 26))
    
    # Calculate yields with improved prediction model
    dirawat_yields = predict_disease_progression(
        hasilsemasa, tahuntuai, total_palms, pokok_sakit, 
        years, rainfall, soil_condition, is_controlled=True
    )
    
    dibiar_yields = predict_disease_progression(
        hasilsemasa, tahuntuai, total_palms, pokok_sakit, 
        years, rainfall, soil_condition, is_controlled=False
    )

    # Create results DataFrame
    df = pd.DataFrame({
        'Tahun': years,
        'Dengan Kawalan (MT)': [round(y, 2) for y in dirawat_yields],
        'Tiada Kawalan (MT)': [round(y, 2) for y in dibiar_yields]
    })

    st.write(df)

    # Visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Line plot - Yield Projection
    ax1.plot(years, dirawat_yields, label='Dengan Kawalan', color='green', marker='o')
    ax1.plot(years, dibiar_yields, label='Tiada Kawalan', color='red', marker='o')
    ax1.set_xlabel('Tahun')
    ax1.set_ylabel('Hasil (MT)')
    ax1.set_title('Unjuran Hasil Mengikut Masa')
    ax1.legend()
    ax1.grid(True)

    # Bar plot - Yearly Losses
    yearly_losses_control = [(dirawat_yields[i-1] - dirawat_yields[i]) 
                           for i in range(1, len(dirawat_yields))]
    yearly_losses_no_control = [(dibiar_yields[i-1] - dibiar_yields[i]) 
                              for i in range(1, len(dibiar_yields))]
    
    x = years[1:]
    width = 0.35
    ax2.bar([x - width/2 for x in x], yearly_losses_control, width, 
            label='Dengan Kawalan', color='green', alpha=0.6)
    ax2.bar([x + width/2 for x in x], yearly_losses_no_control, width, 
            label='Tiada Kawalan', color='red', alpha=0.6)
    ax2.set_xlabel('Tahun')
    ax2.set_ylabel('Kehilangan Hasil (MT)')
    ax2.set_title('Kehilangan Hasil Tahunan')
    ax2
