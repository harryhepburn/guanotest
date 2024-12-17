import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

# Load the datasets
@st.cache_data
def load_data():
    data = pd.read_csv('SYP.csv')
    return data

@st.cache_data
def load_soil_class_data():
    data = pd.read_csv('KELASTANAH.csv')
    return data

def predict_syp(df, rainfall_zone, soil_class, topography, year):
    """
    Predict Site Yield Potential based on input parameters
    """
    # Validate inputs
    filtered_df = df[
        (df['Zon Taburan Hujan'] == rainfall_zone) & 
        (df['Kelas Tanah'] == soil_class) & 
        (df['Topografi'] == topography)
    ]
    
    if filtered_df.empty:
        return None
    
    # Find closest year or interpolate
    closest_year_row = filtered_df.iloc[(filtered_df['Tahun Tuai'] - year).abs().argsort()[:1]]
    
    return closest_year_row['Potensi Hasil'].values[0]

def create_performance_trend_chart(year_data):
    """
    Create an interactive Plotly line chart for performance trend
    """
    # Create interactive Plotly line chart
    fig = px.line(
        year_data, 
        x='Tahun Tuai', 
        y='Potensi Hasil',
        title='Performance Trend',
        labels={
            'Tahun Tuai': 'Planting Year',
            'Potensi Hasil': 'Site Yield Potential (metric tons/hectare)'
        },
        markers=True
    )
    
    # Customize hover template
    fig.update_traces(
        hovertemplate='<b>Planting Year</b>: %{x}<br><b>Yield Potential</b>: %{y:.2f} metric tons/hectare<extra></extra>',
        line=dict(width=3),
        marker=dict(size=8)
    )
    
    # Adjust layout for better readability
    fig.update_layout(
        hovermode='closest',
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        ),
        xaxis_title='Planting Year',
        yaxis_title='Site Yield Potential (metric tons/hectare)',
        height=450
    )
    
    return fig
    
def main():
    st.title('Palm Oil Site Yield Potential (SYP) Calculator')
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs([
        'SYP Calculator', 
        'Soil Classification Lookup', 
        'Performance Trend'
    ])
    
    # Load datasets
    df = load_data()
    soil_class_df = load_soil_class_data()
    
    with tab1:
        # Create columns for input
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Rainfall Zone Selection
            rainfall_zones = df['Zon Taburan Hujan'].unique()
            rainfall_zone = st.selectbox('Rainfall Zone', rainfall_zones)
        
        with col2:
            # Soil Class Selection
            soil_classes = df['Kelas Tanah'].unique()
            soil_class = st.selectbox('Soil Class', soil_classes)
        
        with col3:
            # Topography Selection
            topographies = df['Topografi'].unique()
            topography = st.selectbox('Topography', topographies)
        
        # Year Selection
        max_year = df['Tahun Tuai'].max()
        min_year = df['Tahun Tuai'].min()
        year = st.slider('Planting Year', min_value=min_year, max_value=max_year, value=min_year)
        
        # Calculate Button
        if st.button('Calculate Site Yield Potential'):
            syp = predict_syp(df, rainfall_zone, soil_class, topography, year)
            
            if syp is not None:
                st.success(f'Estimated Site Yield Potential: {syp:.2f} metric tons per hectare')
                
                # Additional Visualization with Plotly
                year_data = df[
                    (df['Zon Taburan Hujan'] == rainfall_zone) & 
                    (df['Kelas Tanah'] == soil_class) & 
                    (df['Topografi'] == topography)
                ]
                
                # Optional: Add some additional insights
                if not year_data.empty:
                    min_yield = year_data['Potensi Hasil'].min()
                    max_yield = year_data['Potensi Hasil'].max()
                    avg_yield = year_data['Potensi Hasil'].mean()
                    
                    st.markdown(f"""
                    ### Yield Insights
                    - **Minimum Yield**: {min_yield:.2f} metric tons/hectare
                    - **Maximum Yield**: {max_yield:.2f} metric tons/hectare
                    - **Average Yield**: {avg_yield:.2f} metric tons/hectare
                    """)
            else:
                st.error('No matching data found. Please adjust your parameters.')
    
    with tab2:
        st.header('Soil Classification Lookup')
        
        # Create columns for filtering
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Kelas Tanah Filter
            kelas_tanah_options = ['All'] + list(soil_class_df['Kelas Tanah'].unique())
            selected_kelas_tanah = st.selectbox('Soil Class', kelas_tanah_options)
        
        with col2:
            # Jenis Tanah Filter
            jenis_tanah_options = ['All'] + list(soil_class_df['Jenis Tanah'].unique())
            selected_jenis_tanah = st.selectbox('Soil Type', jenis_tanah_options)
        
        with col3:
            # Kod Filter
            kod_options = ['All'] + list(soil_class_df['Kod'].unique())
            selected_kod = st.selectbox('Soil Code', kod_options)
        
        with col4:
            # Kumpulan Filter
            kumpulan_options = ['All'] + list(map(str, soil_class_df['Kumpulan'].unique()))
            selected_kumpulan = st.selectbox('Group', kumpulan_options)
        
        # Apply Filters
        filtered_df = soil_class_df.copy()
        
        if selected_kelas_tanah != 'All':
            filtered_df = filtered_df[filtered_df['Kelas Tanah'] == selected_kelas_tanah]
        
        if selected_jenis_tanah != 'All':
            filtered_df = filtered_df[filtered_df['Jenis Tanah'] == selected_jenis_tanah]
        
        if selected_kod != 'All':
            filtered_df = filtered_df[filtered_df['Kod'] == selected_kod]
        
        if selected_kumpulan != 'All':
            filtered_df = filtered_df[filtered_df['Kumpulan'] == int(selected_kumpulan)]
        
        # Display Filtered Results
        st.dataframe(filtered_df, use_container_width=True)
        
        # Summary Statistics
        st.subheader('Summary')
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric('Total Entries', len(filtered_df))
        
        with col2:
            st.metric('Unique Soil Classes', filtered_df['Kelas Tanah'].nunique())
        
        with col3:
            st.metric('Unique Soil Types', filtered_df['Jenis Tanah'].nunique())
        
        with col4:
            st.metric('Unique Groups', filtered_df['Kumpulan'].nunique())
    
    with tab3:
        st.header('Performance Trend Visualization')
        
        # Performance Trend Chart Selection
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Rainfall Zone Selection for Trend
            rainfall_zones = df['Zon Taburan Hujan'].unique()
            trend_rainfall_zone = st.selectbox('Rainfall Zone', rainfall_zones, key='trend_rainfall')
        
        with col2:
            # Soil Class Selection for Trend
            soil_classes = df['Kelas Tanah'].unique()
            trend_soil_class = st.selectbox('Soil Class', soil_classes, key='trend_soil_class')
        
        with col3:
            # Topography Selection for Trend
            topographies = df['Topografi'].unique()
            trend_topography = st.selectbox('Topography', topographies, key='trend_topography')
        
        # Filter data for trend
        trend_data = df[
            (df['Zon Taburan Hujan'] == trend_rainfall_zone) & 
            (df['Kelas Tanah'] == trend_soil_class) & 
            (df['Topografi'] == trend_topography)
        ]
        
        # Create and display Plotly chart
        if not trend_data.empty:
            fig = create_performance_trend_chart(trend_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error('No data available for the selected parameters.')
    
    # Footer
    st.markdown('### Developed by Rafizan Samian - FELDA Strategy & Transformation Department')

if __name__ == '__main__':
    main()
