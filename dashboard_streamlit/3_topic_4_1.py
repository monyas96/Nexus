import streamlit as st
import pandas as pd
import pydeck as pdk

# === Set Page Config ===
# === Section Title & Overview ===
with st.container():
    st.title("📊 Topic 4.1: Public Expenditures")
    st.markdown("""
    Public expenditures focus on how governments allocate resources to essential services such as education, health, and infrastructure.  
    Effective public expenditure management ensures that resources are not wasted and are directed toward development priorities.
    """)

# === Load Data ===
df = pd.read_csv("outputs/master_obt.csv")
ref = pd.read_csv("data/iso3_country_reference.csv").rename(columns={"Country or Area": "country_name"})

# === Country Selection ===
country_list = sorted(df["country_name"].dropna().unique())
selected_country = st.selectbox("🔎 Select a country to explore:", country_list)

# === Map Layout ===
st.markdown("### 🌍 Explore by Region")
map_data = ref.copy()
map_data["selected"] = map_data["country_name"] == selected_country

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v10",
    initial_view_state=pdk.ViewState(latitude=0, longitude=20, zoom=2),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=map_data,
            get_position="[lon, lat]",
            get_radius=40000,
            get_fill_color="[255, 100, 10, 180]",
            pickable=True,
        )
    ],
    tooltip={"text": "{country_name}"}
))

# === Indicator Tabs ===
st.markdown("## 🧭 Indicator Insights")

tab1, tab2 = st.tabs([
    "📌 4.1.1: Public Expenditure Efficiency",
    "📌 4.1.2: Expenditure Quality"
])

# === Tab 1: 4.1.1 ===
with tab1:
    st.markdown("### 📌 4.1.1: Public Public Expenditure Efficiency")
    st.markdown("**Indicator 4.1.1: Aggregate Expenditure Outturn**  \n*Proxy for Public Expenditure Efficiency Index*", unsafe_allow_html=True)

    st.markdown("""
**Definition:**  
This indicator measures how closely actual government expenditures align with the approved budget.  
It reflects the efficiency of fiscal planning and budget execution.

**Relevance:**  
- **Efficiency:** Assesses whether public spending adheres to planned allocations, minimizing budget deviations and cost overruns.  
- **Effectiveness:** Ensures that government expenditure remains within set limits, promoting fiscal discipline and stable public financial management.

**Proxy Justification:**  
The Public Expenditure Efficiency Index (Ratio of actual project costs to budgeted costs) is used to evaluate how well spending follows planned budgets.  
PEFA-WB’s Aggregate Expenditure Outturn is used as a proxy since it directly measures the extent to which government spending aligns with the approved budget.
    """)

    st.info("📊 Graph Placeholder: Aggregate Expenditure Outturn (to be added below)")

# === Tab 2: 4.1.2 ===
with tab2:
    st.markdown("### 📌 4.1.2: Expenditure Quality")
    st.markdown("**Indicator 4.1.2: Expenditure Composition Outturn**  \n*Proxy for Expenditure Quality Score*", unsafe_allow_html=True)

    st.markdown("""
**Definition:**  
This indicator measures whether government expenditures align with policy priorities, ensuring that funds are directed toward critical sectors such as education, health, and infrastructure.

**Relevance:**  
- **Efficiency:** Evaluates if public spending is allocated as planned, reducing inefficiencies and ensuring fiscal responsibility.  
- **Effectiveness:** Demonstrates whether financial resources are used to support sustainable development and social welfare.

**Proxy Justification:**  
The Expenditure Quality Score (Percentage of public spending directed toward development priorities) tracks whether expenditures are used for key sectors.  
PEFA-WB’s Expenditure Composition Outturn is used as a proxy because it assesses if resources are allocated according to national priorities, ensuring minimal waste.
    """)

    st.info("📊 Graph Placeholder: Expenditure Composition Outturn (to be added below)")
