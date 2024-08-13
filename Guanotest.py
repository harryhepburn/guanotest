import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
import io
import base64

def create_pdf_report(data):
    pdf = FPDF()
    pdf.add_page()
    
    # Set font
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "GUANO - Laporan Analisis", 0, 1, "C")
    pdf.ln(10)
    
    # Add content
    pdf.set_font("Arial", "", 12)
    for key, value in data.items():
        pdf.cell(0, 10, f"{key}: {value}", 0, 1)
    
    return pdf.output(dest="S").encode("latin-1")

def main():
    st.set_page_config(page_title="GUANO Calculator", page_icon="🌴", layout="wide")
    
    st.title("GUANO")
    st.subheader("Kalkulator Kos Rawatan Ganoderma")

    st.write("### Kategori Jangkitan Ganoderma:")

    # Create a DataFrame for the categories
    df_categories = pd.DataFrame({
        'Kategori': ['A', 'B', 'C', 'D', 'E', 'F'],
        'Deskripsi': [
            '1. Pokok subur tiada frond skirting<br>2. Masih produktif<br>3. TERDAPAT JASAD BERBUAH',
            '1. Pokok tidak subur<br>2. Simptom frond skirting<br>3. Tidak produktif<br>4. TERDAPAT JASAD BERBUAH',
            '1. Pokok yang telah tumbang<br>2. Patah atas atau bawah<br>3. Mati<br>4. TERDAPAT JASAD BERBUAH',
            '1. Pokok subur atau tidak subur dengan simptom berikut:<br>&nbsp;&nbsp;a. Unopen spears (>3 fronds)<br>&nbsp;&nbsp;b. *Frond skirting*<br>&nbsp;&nbsp;c. Pereputan pada pangkal atau atas<br>2. TIADA JASAD BERBUAH',
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

    colx, col3, col4, col5 = st.columns(4)
    colx.metric("Jumlah Pokok Sihat", pokok_sihat)
    col3.metric("Jumlah Pokok Tidak Sihat", pokok_sakit)
    col4.metric("Pokok Memerlukan 'Soil Mounding'", serangan_a)
    col5.metric("Pokok Memerlukan Sanitasi", sanitasi)

    st.write("---")
    st.subheader("Pengiraan Kos")

    cost_soil_mounding = st.number_input("Kos 'Soil Mounding' per pokok (RM)", min_value=0.0, value=15.0)
    cost_sanitasi = st.number_input("Kos Sanitasi per pokok (RM)", min_value=0.0, value=30.0)

    cost_a = serangan_a * cost_soil_mounding
    cost_b_c = sanitasi * cost_sanitasi
    total_cost = cost_a + cost_b_c

    col6, col7, col8 = st.columns(3)
    col6.metric("Kos 'Soil Mounding'", f"RM {cost_a:.2f}")
    col7.metric("Kos Sanitasi Pokok", f"RM {cost_b_c:.2f}")
    col8.metric("Jumlah Kos", f"RM {total_cost:.2f}")

    st.write("---")
    st.subheader("Anggaran Kerugian Hasil")

    hargaBTS = st.number_input("Harga BTS (RM/MT)", min_value=0.0, value=500.0)
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

    dirawat_yield = hasilsemasa
    dibiar_yield = hasilsemasa
    dirawat_reduction = 0.1
    dibiar_reduction = 0.6

    tahuntuai1 = tahuntuai + 1
    years = list(range(tahuntuai1, 26))
    dirawat_yields = []
    dibiar_yields = []

    for year in years:
        dirawat_yield *= (1 - dirawat_reduction)
        dibiar_yield *= (1 - dibiar_reduction)
        dirawat_yields.append(dirawat_yield)
        dibiar_yields.append(dibiar_yield)

    df = pd.DataFrame({
        'Tahun': years,
        'Kawalan (MT)': dirawat_yields,
        'Tiada Kawalan (MT)': dibiar_yields
    })

    st.write(df)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, dirawat_yields, label='Kawalan')
    ax.plot(years, dibiar_yields, label='Tiada Kawalan')
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Hasil (MT)')
    ax.set_title('Perbandingan Hasil Antara Kawalan dan Tiada Kawalan')
    ax.legend()

    st.pyplot(fig)

    st.write("---")
    st.success("Terima Kasih Kerana Menggunakan GUANO")

    st.write("""
    - Dibangunkan oleh Team KIK Wilayah Raja Alias: **GUANO** 
    - Ahli Kumpulan: Rafizan, Haslina, Izzati, dan Noorain
    - RAhandal
    - SEGALANYA FELDA
    """)

    # Create PDF report
    report_data = {
        "Jumlah Pokok Sihat": pokok_sihat,
        "Jumlah Pokok Tidak Sihat": pokok_sakit,
        "Pokok Memerlukan 'Soil Mounding'": serangan_a,
        "Pokok Memerlukan Sanitasi": sanitasi,
        "Kos 'Soil Mounding'": f"RM {cost_a:.2f}",
        "Kos Sanitasi Pokok": f"RM {cost_b_c:.2f}",
        "Jumlah Kos": f"RM {total_cost:.2f}",
        "Kerugian Hasil Berat BTS": f"{kerugian1:.2f} MT",
        "Kerugian Hasil BTS": f"RM {kerugianRM:.2f}",
        "Hasil Semasa": f"{hasilsemasa:.2f} MT/Tahun"
    }
    
    pdf_report = create_pdf_report(report_data)
    
    # Create download button
    st.download_button(
        label="Muat Turun Laporan PDF",
        data=pdf_report,
        file_name="GUANO_Laporan.pdf",
        mime="application/pdf"
    )

if __name__ == "__main__":
    main()
