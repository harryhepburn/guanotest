import streamlit as st
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
        st.write("### Dibangunkan Oleh:")
        st.write("Rafizan Samian, Jabatan Strategi dan Tranformasi FELDA")

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

            for i, data in enumerate(fertilizer_data):
                st.write(f"### Keputusan untuk Pusingan {i + 1} ({data['type']})")
                
                if data['amount_per_palm'] > 0:
                    total_fertilizer_kg = (data['amount_per_palm'] * total_palms) / 1000  # Convert grams to kg
                    st.write(f"Jumlah baja diperlukan: {total_fertilizer_kg:.2f} kg")

                    # Calculate bags needed (50kg only)
                    bags_needed = math.ceil(total_fertilizer_kg / 50)
                    st.write(f"Jumlah beg (saiz 50kg): {bags_needed}")

                    # Calculate cost
                    if data['price_per_bag'] > 0:
                        cost = bags_needed * data['price_per_bag']
                        st.write(f"Kos keseluruhan (pusingan {i + 1}): RM {cost:.2f}")
                        total_cost += cost

            st.write(f"## 💵 Jumlah Kos Keseluruhan: RM {total_cost:.2f}")
        else:
            st.error("Sila masukkan bilangan pokok dan keluasan kawasan dengan betul.")

if __name__ == "__main__":
    calculate_fertilizer()
