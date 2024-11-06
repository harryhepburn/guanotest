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

def predict_disease_progression(hasilsemasa, tahuntuai, total_palms, infected_palms, years, rainfall, soil_condition, is_controlled=True):
    weather_factor = calculate_weather_factor()
    age_factor = calculate_age_factor(tahuntuai)
    infection_pressure = calculate_infection_pressure(total_palms, infected_palms)
    
    # Adjust for rainfall and soil condition
    rainfall_factor = min(1.0, rainfall / 250)  # Normalize rainfall effect
    soil_factors = {
        "Sangat Baik": 0.7,
        "Baik": 0.8,
        "Sederhana": 0.9,
        "Kurang Baik": 1.0
    }
    soil_factor = soil_factors.get(soil_condition, 0.8)
    
    # Base reduction rates
    if is_controlled:
        base_reduction = 0.1 * (1 + weather_factor) * age_factor * infection_pressure * soil_factor * rainfall_factor
    else:
        base_reduction = 0.6 * (1 + weather_factor) * age_factor * infection_pressure * soil_factor * rainfall_factor
    
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
    
    st.title("GUANO CALCULATOR")
    st.subheader("Kalkulator Kos Rawatan Ganoderma")

    st.write("### Kategori Jangkitan Ganoderma:")

    # Create a DataFrame for the categories
    df_categories = pd.DataFrame({
        'Kategori': ['A', 'B', 'C', 'D', 'E', 'F'],
        'Deskripsi': [
            '1. Pokok subur tiada frond skirting<br>2. Masih produktif<br>3. Ada Jasad Berbuah',
            '1. Pokok tidak subur<br>2. Simptom frond skirting<br>3. Tidak produktif<br>4. Ada Jasad Berbuah',
            '1. Pokok yang telah tumbang<br>2. Patah atas atau bawah<br>3. Mati<br>4. Ada Jasad Berbuah',
            '1. Pokok subur atau tidak subur dengan simptom berikut:<br>&nbsp;&nbsp;a. Unopen spears (>3 fronds)<br>&nbsp;&nbsp;b. Frond skirting<br>&nbsp;&nbsp;c. Pereputan pada pangkal atau atas<br>2. Tiada Jasad Berbuah',
            'Pokok Sihat',
            '1. Pokok selain kategori di atas<br>2. Menunjukkan simptom kekurangan nutrien atau water stress'
        ]
    })

    # Apply styling to the DataFrame
    styled_df = df_categories.style.set_properties(**{
        'text-align': 'left',
        'padding': '10px',
        'border': '1px solid #ddd'
    }).set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'center')]},
        {'selector': 'td', 'props': [('text-align', 'left')]}
    ]).apply(lambda x: ['background-color: #D3D3D3' if i%2==0 else '' for i in range(len(x))], axis=0)

    # Display the styled DataFrame
    st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)

    st.write("---")
    st.subheader("Panduan Bergambar Simptom Ganoderma")

    components.iframe("https://docs.google.com/presentation/d/e/2PACX-1vScJ2zNxKlYKmsZbJkDxOy3ht9knLu_RypRmhgFmdvs8TWGQEksY_F-Gvp20G3Vng/embed?start=false&loop=false&delayms=3000", height=432)
    
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

    st.write("---")
    st.subheader("Hasil Analisis")
    pokok_sakit = serangan_a + serangan_b + serangan_c + serangan_d + serangan_f
    sanitasi = serangan_b + serangan_c
    pokok_sihat = serangan_e
    total_palms = pokok_sakit + pokok_sihat

    colx, col3, col4, col5 = st.columns(4)
    colx.metric("Jumlah Pokok Sihat", pokok_sihat)
    col3.metric("Jumlah Pokok Tidak Sihat", pokok_sakit)
    col4.metric("Pokok Memerlukan 'Soil Mounding'", serangan_a)
    col5.metric("Pokok Memerlukan Sanitasi", sanitasi)

    st.write("---")
    st.subheader("Pengiraan Kos")

    cost_soil_mounding = st.number_input("Kos 'Soil Mounding' per pokok (RM)", min_value=0.0, value=20.0)
    cost_sanitasi = st.number_input("Kos Sanitasi per pokok (RM)", min_value=0.0, value=35.0)

    cost_a = serangan_a * cost_soil_mounding
    cost_b_c = sanitasi * cost_sanitasi
    total_cost = cost_a + cost_b_c

    col6, col7, col8 = st.columns(3)
    col6.metric("Kos 'Soil Mounding'", f"RM {cost_a:.2f}")
    col7.metric("Kos Sanitasi Pokok", f"RM {cost_b_c:.2f}")
    col8.metric("Jumlah Kos", f"RM {total_cost:.2f}")

    st.write("---")
    st.subheader("Anggaran Kerugian Hasil")

    hargaBTS = st.number_input("Harga BTS (RM/MT)", min_value=0.0, value=840.0)
    tahuntuai = st.number_input("Tahun Tuai", min_value=1, max_value=25, value=10)

    kerugian1 = (sanitasi * 0.18) + (serangan_a * 0.8)
    kerugianRM = hargaBTS * kerugian1
    
    col9, col10 = st.columns(2)
    col9.metric("Kerugian Hasil Berat BTS", f"{kerugian1:.2f} MT")
    col10.metric("Kerugian Hasil BTS", f"RM {kerugianRM:.2f}")

    bezarugi = kerugianRM - total_cost
    if kerugianRM > total_cost:
        st.info(f"Jumlah kos adalah kurang daripada kerugian sebanyak RM {bezarugi:.2f}")
    else:
        st.warning(f"Jumlah kos adalah lebih daripada kerugian sebanyak RM {abs(bezarugi):.2f}")

    st.write("---")
    st.subheader("Anggaran Hasil")

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
        hasilsemasa, tahuntuai, total_palms, pokok_sakit, 
        years, rainfall, soil_condition, is_controlled=True
    )
    
    dibiar_yields = predict_disease_progression(
        hasilsemasa, tahuntuai, total_palms, pokok_sakit, 
        years, rainfall, soil_condition, is_controlled=False
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

    st.write("---")
    st.success("Terima Kasih Kerana Menggunakan GUANO")

    st.write("""
    - Dibangunkan oleh Team KIK Wilayah Raja Alias: **BIANGLALA** 
    - Ahli Kumpulan: Rafizan, Haslina, Izzati, Noorain, Baizura, Farah, Andi, dan Amilin
    - Penyelaras: Ariff dan Zamri
    - #RAhandal
    - #SEGALANYA FELDA
    """)

import pandas as pd
import streamlit as st

# Create a DataFrame for the categories
df_categories = pd.DataFrame({
    'Kategori': ['A', 'B', 'C', 'D', 'E', 'F'],
    'Deskripsi': [
        '1. Pokok subur, tiada _frond skirting_<br>2. Masih produktif<br>3. Ada jasad berbuah',
        '1. Pokok tidak subur<br>2. Ada _frond skirting_<br>3. Tidak produktif<br>4. Ada jasad berbuah',
        '1. Pokok yang telah tumbang<br>2. Batang patah di bahagian atas atau bawah<br>3. Mati<br>4. Ada jasad berbuah',
        '1. Pokok tidak subur atau kelihatan _stress_<br>2. Ada _frond skirting_<br>3. Tiada Jasad Berbuah, batang mereput dan miselium putih pada pangkal pokok',
        'Pokok Sihat',
        '1. Pokok selain kategori di atas<br>2. Menunjukkan simptom kekurangan nutrien atau _water stress_'
    ]
})

# Apply styling to the DataFrame
styled_df = df_categories.style.set_properties(**{
    'text-align': 'left',
    'padding': '10px',
    'border': '1px solid #ddd'
}).set_table_styles([
    {'selector': 'th', 'props': [('text-align', 'center')]},
    {'selector': 'td', 'props': [('text-align', 'left')]}
]).apply(lambda x: ['background-color: #D3D3D3' if i % 2 == 0 else '' for i in range(len(x))], axis=0)

# Convert styled DataFrame to HTML and display it in Streamlit
st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
