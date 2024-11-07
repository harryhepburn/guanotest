import streamlit as st
import pandas as pd
import numpy as np

def calculate_ganoderma_impact(
    initial_healthy_palms,
    initial_category_a,
    initial_category_b,
    initial_category_c,
    ffb_price_per_mt,
    starting_year,
    palm_age,
    treatment_cost_per_palm,
    baseline_yield_per_palm=150,  # kg FFB per palm per year for healthy palm
    analysis_years=25
):
    """
    Calculate long-term economic impact of Ganoderma based on academic research.
    
    Parameters:
    - initial_healthy_palms: Number of healthy palms
    - initial_category_a,b,c: Initial number of infected palms by category
    - ffb_price_per_mt: Fresh Fruit Bunch price per metric ton
    - starting_year: Current year of palm age
    - palm_age: Age of palms when analysis starts
    - treatment_cost_per_palm: Cost of treatment per palm
    - baseline_yield_per_palm: Expected yield for healthy palm (kg/palm/year)
    - analysis_years: Number of years to analyze
    
    Returns:
    - DataFrame with yearly projections
    - Summary dictionary
    """
    
    # Constants from research
    DISEASE_SPREAD_RATE = 0.08  # 8% annual increase in infection rate (Flood et al., 2005)
    CATEGORY_A_YIELD_REDUCTION = 0.40  # 40% yield reduction in Category A
    TREATMENT_EFFECTIVENESS = 0.70  # 70% success rate for soil mounding in Category A
    
    # Initialize results DataFrame
    years = range(starting_year, starting_year + analysis_years)
    results = pd.DataFrame(index=years)
    
    # Initialize palm counts
    current_healthy = initial_healthy_palms
    current_cat_a = initial_category_a
    current_cat_b = initial_category_b
    current_cat_c = initial_category_c
    
    # Calculate baseline potential yield accounting for palm age
    def calculate_age_factor(age):
        if age < 3:
            return 0
        elif age < 8:
            return (age - 2) / 6  # Linear increase to peak
        elif age < 15:
            return 1.0  # Peak yield
        else:
            return max(0.8 - (age - 15) * 0.02, 0.4)  # Gradual decline
    
    for year in years:
        current_age = palm_age + (year - starting_year)
        age_yield_factor = calculate_age_factor(current_age)
        
        # Calculate yields
        potential_yield = baseline_yield_per_palm * age_yield_factor
        
        # Calculate yields with and without treatment
        with_treatment_yield = (
            (current_healthy * potential_yield) +
            (current_cat_a * potential_yield * (1 - CATEGORY_A_YIELD_REDUCTION) * TREATMENT_EFFECTIVENESS) +
            (current_cat_b * 0) +  # No yield from Category B
            (current_cat_c * 0)    # No yield from Category C
        ) / 1000  # Convert to MT
        
        without_treatment_yield = (
            (current_healthy * potential_yield) +
            (current_cat_a * 0) +  # Without treatment, Category A palms will die
            (current_cat_b * 0) +
            (current_cat_c * 0)
        ) / 1000  # Convert to MT
        
        # Calculate disease progression
        if year > starting_year:
            new_infections = int(current_healthy * DISEASE_SPREAD_RATE)
            current_healthy -= new_infections
            current_cat_a += new_infections * 0.6  # 60% of new infections are Category A
            current_cat_b += new_infections * 0.3  # 30% of new infections are Category B
            current_cat_c += new_infections * 0.1  # 10% of new infections are Category C
            
            # Progress of existing infections
            cat_a_progression = current_cat_a * 0.2  # 20% of Category A progress to B
            current_cat_a -= cat_a_progression
            current_cat_b += cat_a_progression
            
            cat_b_progression = current_cat_b * 0.3  # 30% of Category B progress to C
            current_cat_b -= cat_b_progression
            current_cat_c += cat_b_progression
        
        # Calculate economics
        treatment_cost = (current_cat_a + current_cat_b) * treatment_cost_per_palm
        revenue_with_treatment = with_treatment_yield * ffb_price_per_mt
        revenue_without_treatment = without_treatment_yield * ffb_price_per_mt
        net_benefit = revenue_with_treatment - revenue_without_treatment - treatment_cost
        
        # Store results
        results.loc[year, 'Healthy Palms'] = current_healthy
        results.loc[year, 'Category A'] = current_cat_a
        results.loc[year, 'Category B'] = current_cat_b
        results.loc[year, 'Category C'] = current_cat_c
        results.loc[year, 'Yield with Treatment (MT)'] = with_treatment_yield
        results.loc[year, 'Yield without Treatment (MT)'] = without_treatment_yield
        results.loc[year, 'Treatment Cost (RM)'] = treatment_cost
        results.loc[year, 'Net Benefit (RM)'] = net_benefit
    
    # Calculate summary statistics
    summary = {
        'total_net_benefit': results['Net Benefit (RM)'].sum(),
        'total_treatment_cost': results['Treatment Cost (RM)'].sum(),
        'cumulative_yield_difference': (
            results['Yield with Treatment (MT)'].sum() - 
            results['Yield without Treatment (MT)'].sum()
        ),
        'years_until_breakeven': (
            results['Net Benefit (RM)'].cumsum().gt(0).idxmax() 
            if (results['Net Benefit (RM)'].cumsum() > 0).any() 
            else None
        )
    }
    
    return results, summary

# Streamlit interface
st.write("---")
st.subheader("Analisis Kos-Faedah Kawalan Ganoderma")

col1, col2 = st.columns(2)
with col1:
    healthy_palms = st.number_input("Bilangan Pokok Sihat", min_value=0, value=100)
    category_a = st.number_input("Bilangan Pokok Kategori A", min_value=0, value=10)
    category_b = st.number_input("Bilangan Pokok Kategori B", min_value=0, value=5)
    category_c = st.number_input("Bilangan Pokok Kategori C", min_value=0, value=2)

with col2:
    ffb_price = st.number_input("Harga BTS (RM/MT)", min_value=0.0, value=840.0)
    palm_age = st.number_input("Umur Pokok (Tahun)", min_value=1, value=10)
    treatment_cost = st.number_input("Kos Rawatan per Pokok (RM)", min_value=0.0, value=50.0)

# Calculate analysis
results, summary = calculate_ganoderma_impact(
    healthy_palms,
    category_a,
    category_b,
    category_c,
    ffb_price,
    palm_age,
    palm_age,
    treatment_cost
)

# Display summary metrics
col3, col4, col5 = st.columns(3)
col3.metric("Jumlah Faedah Bersih", f"RM {summary['total_net_benefit']:,.2f}")
col4.metric("Jumlah Kos Rawatan", f"RM {summary['total_treatment_cost']:,.2f}")
col5.metric("Perbezaan Hasil Kumulatif", f"{summary['cumulative_yield_difference']:,.2f} MT")

if summary['years_until_breakeven']:
    st.success(f"Pelaburan rawatan akan pulang modal dalam {summary['years_until_breakeven'] - palm_age} tahun")
else:
    st.warning("Pelaburan rawatan tidak akan pulang modal dalam tempoh analisis")

# Display detailed results
st.write("### Unjuran Tahunan")
st.dataframe(results.round(2))

# Create visualization
st.write("### Trend Jangkitan dan Hasil")
chart_data = results[['Healthy Palms', 'Category A', 'Category B', 'Category C']].copy()
st.line_chart(chart_data)
