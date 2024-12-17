import pandas as pd
import streamlit as st

# Function to get topography table
def get_topography_table():
    data = {
        "TOPOGRAFI": ["Beralun Lemah", "Beralun Sederhana", "Berbukit"],
        "KOD": ["G", "M", "H"],
        "KETERANGAN": [
            "Kurang Daripada Empat (4) Darjah", 
            "Lima (5) Hingga Dua Belas (12) Darjah", 
            "Melebihi Dua Belas (12) Darjah"
        ]
    }
    return pd.DataFrame(data)

    # Display Topography Table
    st.subheader("Maklumat Topografi")
    topo_df = get_topography_table()
    st.dataframe(topo_df)
    
