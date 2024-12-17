import pandas as pd
import streamlit as st

# Data for the table
data = {
    
    "Jenis Tanah": [
        "SELANGOR", "KANGKONG", "BRIAH", "TELONG", "SEGAMAT", "KUANTAN", "BENTA", "SK. MAS", "KATONG", "SABAK",
        "YONG PENG", "TOM YONG", "KEMUNING", "JERANGAU", "JEMBANG", "JELAI", "CHAMP", "MUSANG", "SEMPAKA",
        "KAMPONG KOLAM", "MASSA", "LENGKAWI", "NENASI", "BATANG MERBAU", "LIMBAT", "TEBOK", "KALLA", "COLLUVIUM",
        "BUKIT", "ORGANIC ALLUVIUM", "LOCAL ALLUVIUM", "BUNGOR", "CHEROK", "SEMUPURNA/IMD", "BATANG", "BESAI",
        "RAU", "TAPAH", "RASAU", "BUNGOR", "ROMPIN", "RUDUA", "MUNCHONG/L", "BUNGOR/S", "DURIAN", "CHENIAN/S",
        "DUTALAN", "BATU LAPAN", "HARRADIL", "MERAPOH/L", "MT. HAIL", "MALACCA", "HARRADS", "GAJAH MATI",
        "MERAPOH", "HARAD/ACAD", "KEDAH", "TAY", "SEREMBAN", "KANTIS", "KALI BUKIT", "DURIAN ALAM", "SEMPORNA/S",
        "BATU/M", "PAGOH", "ORGANIC CLAY MUCK", "SANDY COLLUVIUM", "SRANTI", "KUALA BERANG", "BUKIT TUKU",
        "KAMP. KUBUR", "ULU TIRAM", "JABIL", "SEDIRANG", "MARANG", "TAPAH", "BINA", "KUALA BRANG", "PEAT/D"
    ],
    "Kod": [
        "SLR", "KGR", "BRH", "TLG", "SGT", "KTN", "BNT", "SMS", "KTG", "SBK",
        "YPG", "TYN", "KMG", "JRN", "JMB", "JLC", "CPG", "MUS", "SPA", "KKL",
        "MSI", "LKI", "NBI", "MRB", "LBT", "TBK", "KLL", "COL", "BKT", "ORA",
        "LRA", "BGR", "CRK", "SPAMD", "BTG", "BSH", "RAU", "TGH", "RAS", "RGR", "RPN",
        "RDA", "MUNL", "BRS", "DUR", "CHNS", "DTL", "BNL", "HRDL", "MRPL", "MTH",
        "MLC", "HRDS", "GMH", "MRP", "HRA", "KDH", "TAY", "SRB", "KNT", "KBUK",
        "DAL", "SMP", "BTM", "PGH", "OCM", "SCL", "SRA", "KBG", "BKTK", "KPR",
        "ULT", "JBL", "SDR", "MRG", "TGH", "BNA", "KLG/KBG", "PET/D"
    ],
    "Kumpulan": [
        1, 1, 2, 2, 2, 3, 3, 3, 3, 3,
        3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
        3, 3, 4, 4, 4, 4, 4, 4, 4, 4,
        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
        4, 4, 5, 5, 5, 5, 5, 5, 5, 5,
        5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
        5, 5, 5, 5, 5, 5, 5, 6, 6, 6,
        6, 6, 6, 6, 6, 6, 6
    ]
}

# Create the DataFrame
df = pd.DataFrame(data)

# Streamlit app
st.title("Table Display: Kelas Tanah")

# Display DataFrame as a table
st.dataframe(df)

# Optional: Save the DataFrame to CSV for download
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download Table as CSV", data=csv, file_name="kelas_tanah.csv", mime="text/csv")
