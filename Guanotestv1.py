import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import 
import streamlit.components.v1 as components
from datetime import datetime

def get_rainfall_factor(condition):
    rainfall_factors = {
        "Wet (>200mm/month)": 1.0,
        "Moderate (100-200mm/month)": 0.8,
        "Dry (<100mm/month)": 0.6
    }
    return rainfall_factors.get(condition, 0.8)

def get_soil_factor(soil_class):
    soil_factors = {
        "Class 1 (Best)": 1.0,
        "Class 2 (Moderate)": 0.85,
        "Class 3 (Poor)": 0.7
    }
    return soil_factors.get(soil_class, 0.85)

def calculate_base_yield_potential(age, trees_per_hectare, soil_class):
    # Base yield calculation considering tree density and soil class
    if age < 4:
        return 0  # Immature phase
    elif age < 8:
        base = 25 * get_soil_factor(soil_class)  # Young mature
    elif age < 15:
        base = 30 * get_soil_factor(soil_class)  # Prime age
    else:
        base = 28 * get_soil_factor(soil_class)  # Older palms
    
    # Adjust for tree density
    optimal_density = 136  # optimal trees per hectare
    density_factor = min(1.2, trees_per_hectare / optimal_density)
    
    return base * density_factor

def predict_disease_progression(current_yield, age, total_palms, infected_palms, years, 
                              rainfall_condition, soil_class, trees_per_hectare, is_controlled=True):
    # Get environmental factors
    rainfall_factor = get_rainfall_factor(rainfall_condition)
    soil_factor = get_soil_factor(soil_class)
    
    # Calculate infection pressure
    infection_ratio = infected_palms / total_palms if total_palms > 0 else 0
    infection_pressure = min(0.8, infection_ratio * 1.2)
    
    # Calculate age-based susceptibility
    age_factor = min(1.0, (age / 15) * 0.8)
    
    # Base reduction rates based on academic studies
    if is_controlled:
        base_reduction = 0.08 * infection_pressure * rainfall_factor * soil_factor * age_factor
    else:
        base_reduction = 0.15 * infection_pressure * rainfall_factor * soil_factor * age_factor
    
    yields = [current_yield]
    potential_yields = []
    
    for year in range(len(years)):
        # Calculate potential yield without disease
        potential_yield = calculate_base_yield_potential(age + year, trees_per_hectare, soil_class)
        potential_yields.append(potential_yield)
        
        # Calculate actual yield with disease impact
        cumulative_factor = 1 + (year * 0.03)  # Progressive disease impact
        adjusted_reduction = min(0.9, base_reduction * cumulative_factor)
        
        if is_controlled:
            # Controlled scenario: slower decline and partial recovery possible
            recovery_factor = 0.02 * year if year > 2 else 0
            adjusted_reduction = max(0, adjusted_reduction - recovery_factor)
        
        current_yield *= (1 - adjusted_reduction)
        # Ensure yield doesn't fall below 10% of potential
        current_yield = max(current_yield, potential_yield * 0.1)
        yields.append(current_yield)
    
    return yields[1:], potential_yields

def main():
    st.set_page_config(page_title="GUANO Calculator", page_icon="🌴", layout="wide")
    
    st.title("GUANO CALCULATOR")
    st.subheader("Kalkulator Kos Rawatan Ganoderma")

    # Categories section
    st.write("### Kategori Jangkitan Ganoderma:")
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

    styled_df = df_categories.style.set_properties(**{
        'text-align': 'left',
        'padding': '10px',
        'border': '1px solid #ddd'
    }).set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'center')]},
        {'selector': 'td', 'props': [('text-align', 'left')]}
    ]).apply(lambda x: ['background-color: #D3D3D3' if i%2==0 else '' for i in range(len(x))], axis=0)

    st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)

    # Visual guide
    st.write("---")
    st.subheader("Panduan Bergambar Simptom Ganoderma")
    components.iframe("https://docs.google.com/presentation/d/e/2PACX-1vScJ2zNxKlYKmsZbJkDxOy3ht9knLu_RypRmhgFmdvs8TWGQEksY_F-Gvp20G3Vng/embed?start=false&loop=false&delayms=3000", height=432)
    
    # Farm Information
    st.write("---")
    st.subheader("Maklumat Ladang")
    
    col1, col2 = st.columns(2)
    with col1:
        trees_per_hectare = st.number_input("Bilangan Pokok Per Hektar", 
                                          min_value=100, max_value=160, value=136)
        current_yield = st.number_input("Hasil Semasa (MT/Hektar/Tahun)", 
                                      min_value=0.0, value=20.0)
        tahuntuai = st.number_input("Umur Sawit (Tahun)", min_value=1, max_value=25, value=10)
    
    with col2:
        rainfall_condition = st.selectbox("Keadaan Hujan",
                                        ["Basah (>200mm/month)", 
                                         "Sederhana (100-200mm/month)",
                                         "Kering (<100mm/month)"])
        soil_class = st.selectbox("Kelas Tanah",
                                ["Kelas 1", 
                                 "Kelas 2", 
                                 "Kelas 3"])

    # Census section
    st.write("---")
    st.subheader("Bancian")

    col3, col4 = st.columns(2)
    with col3:
        serangan_a = st.number_input("Bilangan Pokok Kategori A", min_value=0, value=0)
        serangan_b = st.number_input("Bilangan Pokok Kategori B", min_value=0, value=0)
        serangan_c = st.number_input("Bilangan Pokok Kategori C", min_value=0, value=0)

    with col4:
        serangan_d = st.number_input("Bilangan Pokok Kategori D", min_value=0, value=0)
        serangan_e = st.number_input("Bilangan Pokok Kategori E", min_value=0, value=0)
        serangan_f = st.number_input("Bilangan Pokok Kategori F", min_value=0, value=0)

    
    # Create data for pie chart
    data = {
        'Kategori A': serangan_a,
        'Kategori B': serangan_b,
        'Kategori C': serangan_c,
        'Kategori D': serangan_d,
        'Kategori E': serangan_e,
        'Kategori F': serangan_f
    }

    # Create pie chart using matplotlib
    total = sum(data.values())
    if total > 0:  # Only show chart if there's data
        plt.figure(figsize=(10, 8))
        plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
        plt.title('Taburan Kategori')
        st.pyplot(plt)
        plt.close()
          
    
    # Analysis results
    st.write("---")
    st.subheader("Hasil Analisis")
    pokok_sakit = serangan_a + serangan_b + serangan_c + serangan_d + serangan_f
    sanitasi = serangan_b + serangan_c
    pokok_sihat = serangan_e
    total_palms = pokok_sakit + pokok_sihat

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Jumlah Pokok Sihat", pokok_sihat)
    col6.metric("Jumlah Pokok Sakit", pokok_sakit)
    col7.metric("Pokok Memerlukan _Soil Mounding_", serangan_a)
    col8.metric("Pokok Memerlukan Sanitasi", sanitasi)

    # Cost calculation
    st.write("---")
    st.subheader("Pengiraan Kos")

    cost_soil_mounding = st.number_input("Kos 'Soil Mounding' per pokok (RM)", min_value=0.0, value=20.0)
    cost_sanitasi = st.number_input("Kos Sanitasi per pokok (RM)", min_value=0.0, value=35.0)

    cost_a = serangan_a * cost_soil_mounding
    cost_b_c = sanitasi * cost_sanitasi
    total_cost = cost_a + cost_b_c

    col9, col10, col11 = st.columns(3)
    col9.metric("Kos _Soil Mounding_", f"RM {cost_a:.2f}")
    col10.metric("Kos Sanitasi Pokok", f"RM {cost_b_c:.2f}")
    col11.metric("Jumlah Kos", f"RM {total_cost:.2f}")

    # Yield prediction
    st.write("---")
    st.subheader("Anggaran Hasil")
    
    years = list(range(tahuntuai + 1, 26))
    
    dirawat_yields, potential_yields = predict_disease_progression(
        current_yield, tahuntuai, total_palms, pokok_sakit,
        years, rainfall_condition, soil_class, trees_per_hectare, is_controlled=True
    )
    
    dibiar_yields, _ = predict_disease_progression(
        current_yield, tahuntuai, total_palms, pokok_sakit,
        years, rainfall_condition, soil_class, trees_per_hectare, is_controlled=False
    )
    
    # Results display
    df_results = pd.DataFrame({
        'Tahun': years,
        'Potensi Hasil (MT/Ha)': [round(y, 2) for y in potential_yields],
        'Dengan Kawalan (MT/Ha)': [round(y, 2) for y in dirawat_yields],
        'Tanpa Kawalan (MT/Ha)': [round(y, 2) for y in dibiar_yields]
    })
    
    st.write(df_results)
    
    # Visualizations
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    ax1.plot(years, potential_yields, label='Potensi Hasil', color='blue', linestyle='--')
    ax1.plot(years, dirawat_yields, label='Dengan Kawalan', color='green', marker='o')
    ax1.plot(years, dibiar_yields, label='Tanpa Kawalan', color='red', marker='o')
    ax1.set_xlabel('Tahun')
    ax1.set_ylabel('Hasil (MT/Ha)')
    ax1.set_title('Perbandingan Hasil')
    ax1.legend()
    ax1.grid(True)
    
    potential_loss_control = [p - d for p, d in zip(potential_yields, dirawat_yields)]
    potential_loss_no_control = [p - d for p, d in zip(potential_yields, dibiar_yields)]
    
    width = 0.35
    x = np.array(years)
    ax2.bar(x - width/2, potential_loss_control, width,
            label='Kehilangan Dengan Kawalan', color='green', alpha=0.6)
    ax2.bar(x + width/2, potential_loss_no_control, width,
            label='Kehilangan Tanpa Kawalan', color='red', alpha=0.6)
    ax2.set_xlabel('Tahun')
    ax2.set_ylabel('Kehilangan Hasil (MT/Ha)')
    ax2.set_title('Kehilangan Hasil Berbanding Potensi')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    st.pyplot(fig)


    # Modified Cost-Benefit Analysis section
    st.write("---")
    st.subheader("Analisis Kos-Faedah")

    hargaBTS = st.number_input("Harga BTS Semasa (RM/MT)", min_value=0.0, value=840.0)
    
    # Calculate yield losses using the prediction data
    yearly_loss_control = [d - c for c, d in zip(dirawat_yields, dibiar_yields)]
    cumulative_loss_5yr = sum(yearly_loss_control[:5])  # First 5 years of losses
    
    kerugianRM = hargaBTS * cumulative_loss_5yr
    bezarugi = kerugianRM - total_cost

    # Display results in columns
    col_loss1, col_loss2, col_loss3 = st.columns(3)
    col_loss1.metric("Anggaran Kehilangan BTS (5 Tahun)", f"{cumulative_loss_5yr:.2f} MT")
    col_loss2.metric("Kerugian dalam RM", f"RM {kerugianRM:.2f}")
    col_loss3.metric("Perbezaan Kos-Kerugian", f"RM {abs(bezarugi):.2f}")

    # Show detailed year-by-year analysis
    st.write("#### Analisis Kerugian Tahunan")
    
    yearly_data = pd.DataFrame({
        'Tahun': years[:5],  # First 5 years
        'Kehilangan BTS (MT/Ha)': [round(loss, 2) for loss in yearly_loss_control[:5]],
        'Kerugian (RM)': [round(loss * hargaBTS, 2) for loss in yearly_loss_control[:5]]
    })
    
    st.write(yearly_data)

    # Show cost-benefit analysis message
    if kerugianRM > total_cost:
        st.success(f"""
        💰 Rawatan adalah BERBALOI kerana:
        - Kos rawatan (RM {total_cost:.2f}) adalah lebih rendah berbanding anggaran kerugian 5 tahun (RM {kerugianRM:.2f})
        - Potensi penjimatan sebanyak RM {bezarugi:.2f} dalam tempoh 5 tahun dengan melakukan rawatan
        - Purata penjimatan tahunan: RM {(bezarugi/5):.2f}
        """)
    else:
        st.warning(f"""
        ⚠️ Pertimbangkan semula kos rawatan kerana:
        - Kos rawatan (RM {total_cost:.2f}) adalah lebih tinggi berbanding anggaran kerugian 5 tahun (RM {kerugianRM:.2f})
        - Kos tambahan sebanyak RM {abs(bezarugi):.2f} diperlukan untuk rawatan
        - Purata kerugian tahunan: RM {abs(bezarugi/5):.2f}
        """)

    # Enhanced visualization
    fig_cost = plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    labels = ['Kos Rawatan', 'Kerugian 5 Tahun']
    values = [total_cost, kerugianRM]
    colors = ['#2ecc71' if kerugianRM > total_cost else '#e74c3c', '#3498db']
    
    plt.bar(labels, values, color=colors)
    plt.title('Perbandingan Kos Rawatan vs Kerugian 5 Tahun')
    plt.ylabel('RM')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels on top of each bar
    for i, v in enumerate(values):
        plt.text(i, v, f'RM {v:,.2f}', ha='center', va='bottom')

    # Add yearly loss trend
    plt.subplot(1, 2, 2)
    years_plot = years[:5]
    yearly_losses = [loss * hargaBTS for loss in yearly_loss_control[:5]]
    plt.plot(years_plot, yearly_losses, marker='o', color='#3498db', linewidth=2)
    plt.fill_between(years_plot, yearly_losses, alpha=0.3, color='#3498db')
    plt.title('Trend Kerugian Tahunan')
    plt.xlabel('Tahun')
    plt.ylabel('Kerugian (RM)')
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    st.pyplot(fig_cost)


    
    # Credits
    st.write("---")
    st.success("Terima Kasih Kerana Menggunakan GUANO")
    st.write("""
    - Dibangunkan oleh Team KIK Wilayah Raja Alias: **BIANGLALA** 
    - Ahli Kumpulan: Rafizan, Haslina, Izzati, Noorain, Baizura, Farah, Andi, dan Amilin
    - Penyelaras: Ariff dan Zamri
    - #RAhandal
    - #SEGALANYA FELDA
    """)

if __name__ == "__main__":
    main()
