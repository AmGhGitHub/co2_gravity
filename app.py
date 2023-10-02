import math

import streamlit as st

# Streamlit UI
st.title("Gravity Override in Vertical CO2 Injectors")

# Getting user input
kv_kh_ratio = st.number_input(
    "kv/kh ratio:", value=0.01, step=0.0001, min_value=0.001, format="%.3f"
)
res_thickness = st.number_input(
    "Reservoir thickness (m)", value=200.0, step=1.0, min_value=1.0
)
rhoWater = st.number_input(
    "Brine density (kg/m3):", value=1103.0, step=10.0, min_value=500.0
)  # typical value for water is around 1000 kg/m^3
rhoCO2 = st.number_input(
    "CO2 density (kg/m3):", value=460.8, step=10.0, min_value=100.0
)  # typical value for CO2 at sea level, 15°C is around 1.225 kg/m^3
qinj = st.number_input(
    "qCO2 (sE6m3/day)", value=1.5, step=0.1, max_value=10.0, min_value=0.1
)
bg_co2 = st.number_input(
    "CO2 FVF (rm3/sm3)", value=4.05993e-03, step=0.00001, format="%.6f"
)

# Calculation based on user input
result = (
    (1 / kv_kh_ratio)
    * qinj
    * 1e6
    * bg_co2
    / ((rhoWater - rhoCO2) * 9.81 * res_thickness * 2 * math.pi)
)

# Display the result
st.write(
    "The calculated critical radius for gravity ovveride is:", round(result, 4), "m"
)
