import math

import streamlit as st
from streamlit_echarts import st_echarts

st.set_page_config(layout="wide")

# Streamlit UI
st.title("Gravity Override in Vertical CO2 Injectors")

# Divide into three columns: injection, reservoir properties, fluid properties
col_injection, col_reservoir, col_fluid = st.columns(3)

# Injection column inputs
with col_injection:
    st.subheader("Injection")
    qinj = st.number_input(
        "qCO2 (sE6m3/day)", value=1.5, step=0.1, max_value=10.0, min_value=0.1
    )
    bg_co2 = st.number_input(
        "CO2 FVF (rm3/sm3)", value=4.05993e-03, step=0.00001, format="%.6f"
    )

# Reservoir properties column inputs
with col_reservoir:
    st.subheader("Reservoir properties")
    kv_kh_ratio = st.number_input(
        "kv/kh ratio:", value=0.01, step=0.0001, min_value=0.001, format="%.3f"
    )
    res_thickness = st.number_input(
        "Reservoir thickness (m)", value=200.0, step=1.0, min_value=1.0
    )

# Fluid properties column inputs
with col_fluid:
    st.subheader("Fluid properties")
    rhoCO2 = st.number_input(
        "CO2 density (kg/m3):", value=460.8, step=10.0, min_value=100.0
    )
    rhoWater = st.number_input(
        "Brine density (kg/m3):", value=1103.0, step=10.0, min_value=500.0
    )

# Calculation based on user input
result = (
    qinj
    * 1e6
    * bg_co2
    / (kv_kh_ratio * (rhoWater - rhoCO2) * 9.81 * res_thickness * 2 * math.pi)
)


# values1 = [i / 100 for i in range(1, 10)]
values2 = [i / 10 for i in range(1, 10)]

# For values between 1 to 200 in 1 increment
values3 = list(range(1, int(res_thickness) + 1))

# Combine the two lists
h_values = values2 + values3


rc_values = [
    round(
        qinj
        * 1e6
        * bg_co2
        / (kv_kh_ratio * (rhoWater - rhoCO2) * 9.81 * h * 2 * math.pi),
        4,
    )
    for h in h_values
]

all_results = [[rc_value, h_value] for (h_value, rc_value) in zip(h_values, rc_values)]


st.markdown(
    f'<span style="font-size: 20px; color: black;">The calculated critical radius at reservoir bottom: </span>'
    f'<span style="font-size: 20px; color: green;">{round(result, 4)}</span>'
    f'<span style="font-size: 20px; color: black;"> m</span>',
    unsafe_allow_html=True,
)


col_graph1, col_graph2 = st.columns(2)

with col_graph1:
    st.subheader("semi-log plot")
    options = {
        "xAxis": {
            "type": "log",
            "position": "top",
            "inverse": False,
            "name": "rc (m)",  # Add this line
            "nameLocation": "middle",  # Add this line
            "nameGap": 25,
        },
        "yAxis": {
            "type": "value",
            "inverse": True,
            "name": "h (m)",
            "nameLocation": "middle",
            "nameGap": 30,
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross", "crossStyle": {"color": "#999"}},
        },
        "series": [{"data": all_results, "type": "line"}],
    }

    st_echarts(options=options, key="echarts1", height="500px")

with col_graph2:
    st.subheader("log-log plot")
    options = {
        "xAxis": {
            "type": "log",
            "position": "top",
            "inverse": False,
            "name": "rc (m)",  # Add this line
            "nameLocation": "middle",  # Add this line
            "nameGap": 25,
        },
        "yAxis": {
            "inverse": True,
            "type": "log",
            "name": "h (m)",
            "nameLocation": "middle",
            "nameGap": 20,
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross", "crossStyle": {"color": "#999"}},
        },
        "series": [{"data": all_results, "type": "line"}],
    }

    st_echarts(options=options, key="echarts2", height="500px")

st.markdown(
    '<p style="text-align: right; font-size: 12px ;color:red;">Amir Ghaderi, Oct. 2, 2023</p>',
    unsafe_allow_html=True,
)
