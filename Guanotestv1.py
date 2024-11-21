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
    
    # Rest of the code remains the same as in the original script
    # ... [keep the rest of the main() function unchanged]

if __name__ == "__main__":
    main()
