import streamlit as st
import pandas as pd
import math

def calculate_fertilizer():
    st.set_page_config(page_title="Kalkulator Baja Kelapa Sawit", page_icon="🌾", layout="centered")

    st.title("Kalkulator Keperluan Baja Kelapa Sawit 🌾")
    st.write("Selamat datang ke aplikasi kalkulator baja! Aplikasi ini membantu anda mengira keperluan baja untuk ladang kelapa sawit dengan mudah dan pantas.")

    # Sidebar information
    with st.sidebar:
        st.header("Tentang Aplikasi")
        st.write(
            "Aplikasi ini direka untuk membantu pekebun kelapa sawit mengira jumlah keperluan baja, bilangan beg baja, dan kos keseluruhan berdasarkan maklumat yang dimasukkan."
        )
        st.write("### Cara Penggunaan:")
        st.write("1. Masukkan maklumat untuk setiap pusingan pembajaan.")
        st.write("2. Masukkan bilangan pokok sawit per hektar dan jumlah kawasan.")
        st.write("3. Klik butang 'Kira Keperluan Baja' untuk melihat hasilnya.")
        st.write("### Pembangun:")
        st.write("Rafizan Samian, Jabatan SS")

    # Input rounds of fertilization
    num_rounds = st.number_input("Bilangan pusingan pembajaan:", min_value=1, step=1, value=1)

    fertilizer_data = []

    for i in range(1, num_rounds + 1):
        st.write(f"### Pusingan {i}")
        fertilizer_type = st.text_input(f"Jenis baja untuk pusingan {i}:", key=f"fertilizer_type_{i}")
        amount_per_palm = st.number_input(f"Jumlah baja per pokok (gram):", min_value=0.0, step=0.1, value=0.0, key=f"amount_per_palm_{i}")
        price_per_bag = st.number_input(f"Harga satu beg baja (RM):", min_value=0.0, step=0.1, value=0.0, key=f"price_per_bag_{i}")
        fertilizer_data.append({
            "type": fertilizer_type,
            "amount_per_palm": amount_per_palm,
            "price_per_bag": price_per_bag,
        })

    # Input number of palms and area size
    st.write("## Maklumat Ladang")
    num_palms_per_hectare = st.number_input("Bilangan pokok sawit per hektar:", min_value=0, step=1, value=0)
    total_area = st.number_input("Jumlah kawasan (hektar):", min_value=0.0, step=0.1, value=0.0)

    if st.button("🌱 Kira Keperluan Baja"):
        if total_area > 0 and num_palms_per_hectare > 0:
            total_palms = num_palms_per_hectare * total_area
            st.success(f"Jumlah pokok sawit: {total_palms}")

            total_cost = 0.0
            results = []

            for i, data in enumerate(fertilizer_data):
                if data['amount_per_palm'] > 0:
                    total_fertilizer_kg = (data['amount_per_palm'] * total_palms) / 1000  # Convert grams to kg
                    bags_needed = math.ceil(total_fertilizer_kg / 50)  # Calculate bags needed (50kg only)

                    # Calculate cost
                    cost = bags_needed * data['price_per_bag'] if data['price_per_bag'] > 0 else 0
                    total_cost += cost

                    results.append({
                        "Pusingan": i + 1,
                        "Jenis Baja": data['type'],
                        "Jumlah Baja (kg)": total_fertilizer_kg,
                        "Jumlah Beg (50kg)": bags_needed,
                        "Kos (RM)": cost,
                    })

            # Display results as a table
            results_df = pd.DataFrame(results)
            st.write("## Keputusan Pembajaan")
            st.dataframe(results_df, use_container_width=True)

            # Total cost
            st.write(f"## 💵 Jumlah Kos Keseluruhan: RM {total_cost:.2f}")

            # Download option
            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Muat Turun Keputusan",
                data=csv,
                file_name="keputusan_pembajaan.csv",
                mime="text/csv",
            )
        else:
            st.error("Sila masukkan bilangan pokok dan keluasan kawasan dengan betul.")

if __name__ == "__main__":
    calculate_fertilizer()
