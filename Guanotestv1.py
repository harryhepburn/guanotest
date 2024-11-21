import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

def about_page():
    st.header("🍄 GUANO Calculator - Ganoderma Management Tool")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://raw.githubusercontent.com/Andi-getch/icons/main/ganoderma-icon.png", width=200)
    
    with col2:
        st.markdown("""
        ### About the Project
        GUANO Calculator is an innovative tool designed to help plantation managers 
        assess and manage Ganoderma infections in oil palm plantations.

        #### Key Features:
        - 📊 Categorize palm tree health status
        - 💰 Estimate treatment costs
        - 📈 Predict yield loss
        - 🌴 Comprehensive analysis
        """)
    
    st.write("---")
    
    st.subheader("Our Team: BIANGLALA")
    team_members = [
        "Rafizan", "Haslina", "Izzati", "Noorain", 
        "Baizura", "Farah", "Andi", "Amilin"
    ]
    
    # Display team members in a grid
    cols = st.columns(4)
    for i, member in enumerate(team_members):
        cols[i % 4].markdown(f"- {member}")
    
    st.write("---")
    
    st.subheader("Advisors")
    st.markdown("""
    - Ariff
    - Zamri
    
    #RAhandal | #SEGALANYA FELDA
    """)

def main():
    # Set page configuration with Ganoderma icon
    st.set_page_config(
        page_title="GUANO Calculator", 
        page_icon="🍄", 
        layout="wide"
    )
    
    # Sidebar for navigation
    st.sidebar.title("🍄 GUANO Calculator")
    menu = st.sidebar.radio(
        "Navigate", 
        ["Calculator", "About", "Help"], 
        index=0
    )
    
    if menu == "About":
        about_page()
        return
    
    elif menu == "Help":
        st.header("🆘 Help & Guide")
        st.markdown("""
        ### How to Use GUANO Calculator
        
        1. **Kategorize Palm Trees**
           - Input the number of palm trees in each health category (A-F)
           - Refer to the category descriptions below
        
        2. **Cost Estimation**
           - Set the cost for Soil Mounding and Sanitization
           - Calculate total treatment costs
        
        3. **Yield Loss Estimation**
           - Input current BTS price
           - Specify harvest year
           - See potential yield loss and financial impact
        """)
        
        st.info("For detailed guidance, check the pictorial guide in the main calculator page.")
        return
    
    # Main Calculator Page
    st.title("GUANO CALCULATOR 🍄")
    st.subheader("Kalkulator Kos Rawatan Ganoderma")

    st.write("### Kategori Jangkitan Ganoderma:")

    # Create a DataFrame for the categories
    df_categories = pd.DataFrame({
        'Kategori': ['A', 'B', 'C', 'D', 'E', 'F'],
        'Deskripsi': [
            '1. Pokok subur, tiada frond skirting<br>2. Masih produktif<br>3. Ada jasad berbuah',
            '1. Pokok tidak subur<br>2. Ada frond skirting<br>3. Tidak produktif<br>4. Ada jasad berbuah',
            '1. Pokok yang telah tumbang<br>2. Batang patah di bahagian atas atau bawah<br>3. Mati<br>4. Ada jasad berbuah',
            '1. Pokok tidak subur atau kelihatan stress<br>2. Ada frond skirting<br>3. Tiada Jasad Berbuah<br>4. Tiada batang mereput dan miselium putih pada pangkal pokok',
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

    # Slide show embedded
    components.iframe("https://docs.google.com/presentation/d/e/2PACX-1vScJ2zNxKlYKmsZbJkDxOy3ht9knLu_RypRmhgFmdvs8TWGQEksY_F-Gvp20G3Vng/embed?start=false&loop=false&delayms=3000", height=432)

    st.write("---")
    st.subheader("Bancian")

    col1, col2 = st.columns(2)

    with col1:
        serangan_a = st.number_input("Bilangan Pokok Kategori A", min_value=0, value=0, help="Healthy palms requiring soil mounding")
        serangan_b = st.number_input("Bilangan Pokok Kategori B", min_value=0, value=0, help="Unproductive palms needing attention")
        serangan_c = st.number_input("Bilangan Pokok Kategori C", min_value=0, value=0, help="Fallen or dead palms")

    with col2:
        serangan_d = st.number_input("Bilangan Pokok Kategori D", min_value=0, value=0, help="Stressed palms with no visible decay")
        serangan_e = st.number_input("Bilangan Pokok Kategori E", min_value=0, value=0, help="Completely healthy palms")
        serangan_f = st.number_input("Bilangan Pokok Kategori F", min_value=0, value=0, help="Palms with nutrient or water stress")

    # Create data for pie chart
    data = {
        'Kategori A': serangan_a,
        'Kategori B': serangan_b,
        'Kategori C': serangan_c,
        'Kategori D': serangan_d,
        'Kategori E': serangan_e,
        'Kategori F': serangan_f
    }
    
    # Create pie chart using plotly
    total = sum(data.values())
    if total > 0:  # Only show chart if there's data
        fig = px.pie(
            values=list(data.values()),
            names=list(data.keys()),
            title='Taburan Kategori',
            labels={'label': 'Kategori', 'value': 'Bilangan Pokok'}
        )
        st.plotly_chart(fig)
    
    st.write("---")
    st.subheader("Hasil Analisis")
    pokok_sakit = serangan_a + serangan_b + serangan_c + serangan_d + serangan_f
    sanitasi = serangan_b + serangan_c
    pokok_sihat = serangan_e

    colx, col3, col4, col5 = st.columns(4)
    colx.metric("Jumlah Pokok Sihat", pokok_sihat)
    col3.metric("Jumlah Pokok Tidak Sihat", pokok_sakit)
    col4.metric("Pokok Memerlukan _Soil Mounding_", serangan_a)
    col5.metric("Pokok Memerlukan Sanitasi", sanitasi)

    st.write("---")
    st.subheader("Pengiraan Kos")

    cost_soil_mounding = st.number_input("Kos _Soil Mounding_ per pokok (RM)", min_value=0.0, value=20.0)
    cost_sanitasi = st.number_input("Kos Sanitasi per pokok (RM)", min_value=0.0, value=35.0)

    cost_a = serangan_a * cost_soil_mounding
    cost_b_c = sanitasi * cost_sanitasi
    total_cost = cost_a + cost_b_c

    col6, col7, col8 = st.columns(3)
    col6.metric("Kos _Soil Mounding_", f"RM {cost_a:.2f}")
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

    dirawat_yield = hasilsemasa
    dibiar_yield = hasilsemasa
    dirawat_reduction = 0.05
    dibiar_reduction = 0.2

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
    st.write('Nota: Andaian pengurangan hasil sehingga 20% setahun jika dibiar tanpa kawalan dan 5% jika dikawal.')

    #fig, ax = plt.subplots(figsize=(4, 2.5))
    #ax.plot(years, dirawat_yields, label='Kawalan', color='green', marker='x', markersize=4, linewidth=1.5)
    #ax.plot(years, dibiar_yields, label='Tiada Kawalan', color='red', marker='o', markersize=4, linewidth=1.5)
    ##ax.set_xlabel('Tahun', fontsize=8)
    #ax.set_ylabel('Hasil (MT)', fontsize=8)
    #ax.set_title('Perbandingan Hasil Antara Kawalan dan Tiada Kawalan', fontsize=9)
    #ax.legend(fontsize=7)
    #ax.grid(True, linestyle='--', alpha=0.7)
    #ax.tick_params(axis='both', labelsize=7)  # Make tick labels smaller

    # Adjust layout to prevent label cutoff
    #plt.tight_layout()
    
    #st.pyplot(fig)

    #####
    
    

    # Create the figure
    fig = go.Figure()

    # Add traces for both lines
    fig.add_trace(
        go.Scatter(
            x=years, 
            y=dirawat_yields, 
            name='Kawalan',
            line=dict(color='green', width=2),
            mode='lines+markers',
            marker=dict(symbol='x', size=6)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=years, 
            y=dibiar_yields, 
            name='Tiada Kawalan',
            line=dict(color='red', width=2),
            mode='lines+markers',
            marker=dict(symbol='circle', size=6)
        )
    )

    # Update layout
    fig.update_layout(
        title=dict(
            text='Perbandingan Hasil Antara Kawalan dan Tiada Kawalan',
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=14)
        ),
        xaxis_title='Tahun',
        yaxis_title='Hasil (MT)',
        width=500,    
        height=300,   
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        margin=dict(l=50, r=50, t=50, b=50),
        template='plotly_white',
        plot_bgcolor='white'
        )

    # Add grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)
    ###

    st.write("---")
    st.success("Terima Kasih Kerana Menggunakan GUANO")


if __name__ == "__main__":
    main()
