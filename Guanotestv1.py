import streamlit as st
import math

def calculate_fertilizer():
    st.title("Kalkulator Keperluan Baja Kelapa Sawit")
    st.write("Aplikasi ini membantu mengira keperluan baja untuk kelapa sawit berdasarkan bilangan pokok, kawasan hektar, dan jenis baja.")

    # Input rounds of fertilization
    num_rounds = st.number_input("Bilangan pusingan pembajaan:", min_value=1, step=1, value=1)

    fertilizer_data = []

    for i in range(1, num_rounds + 1):
        st.write(f"### Pusingan {i}")
        fertilizer_type = st.text_input(f"Jenis baja untuk pusingan {i}:", key=f"fertilizer_type_{i}")
        amount_per_palm = st.number_input(f"Jumlah baja per pokok (gram) untuk pusingan {i}:", min_value=0.0, step=0.1, value=0.0, key=f"amount_per_palm_{i}")
        price_per_bag = st.number_input(f"Harga satu beg baja (dalam RM) untuk pusingan {i}:", min_value=0.0, step=0.1, value=0.0, key=f"price_per_bag_{i}")
        fertilizer_data.append({
            "type": fertilizer_type,
            "amount_per_palm": amount_per_palm,
            "price_per_bag": price_per_bag,
        })

    # Input number of palms and area size
    num_palms_per_hectare = st.number_input("Bilangan pokok sawit per hektar:", min_value=0, step=1, value=0)
    total_area = st.number_input("Jumlah kawasan (hektar):", min_value=0.0, step=0.1, value=0.0)

    # Bag size options
    bag_sizes = [25, 50]  # kg per bag

    if st.button("Kira Keperluan Baja"):
        if total_area > 0 and num_palms_per_hectare > 0:
            total_palms = num_palms_per_hectare * total_area
            st.write(f"Jumlah pokok sawit: {total_palms}")

            total_cost = 0.0

            for i, data in enumerate(fertilizer_data):
                st.write(f"### Keputusan untuk Pusingan {i + 1} ({data['type']})")
                
                if data['amount_per_palm'] > 0:
                    total_fertilizer_kg = (data['amount_per_palm'] * total_palms) / 1000  # Convert grams to kg
                    st.write(f"Jumlah baja diperlukan: {total_fertilizer_kg:.2f} kg")

                    # Calculate bags needed
                    bags_needed = {size: math.ceil(total_fertilizer_kg / size) for size in bag_sizes}

                    for size, bags in bags_needed.items():
                        st.write(f"Jumlah beg (saiz {size}kg): {bags}")

                    # Calculate cost
                    if data['price_per_bag'] > 0:
                        bag_size = st.selectbox(f"Pilih saiz beg untuk pengiraan kos (pusingan {i + 1}):", bag_sizes, key=f"bag_size_{i}")
                        cost = bags_needed[bag_size] * data['price_per_bag']
                        st.write(f"Kos keseluruhan (pusingan {i + 1}): RM {cost:.2f}")
                        total_cost += cost

            st.write(f"## Jumlah Kos Keseluruhan: RM {total_cost:.2f}")
        else:
            st.error("Sila masukkan bilangan pokok dan keluasan kawasan dengan betul.")

if __name__ == "__main__":
    calculate_fertilizer()
