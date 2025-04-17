import streamlit as st
import pandas as pd
import pydeck as pdk

# === Set Page Config ===
st.set_page_config(page_title="Topic 4.2: Budget and Tax Revenues", layout="wide")

# === Section Title & Overview ===
with st.container():
    st.title("📊 Topic 4.2: Budget and Tax Revenues")
    st.markdown("""
    Budget and tax revenues are crucial for ensuring that governments have the financial resources necessary to fund essential services and development initiatives.  
    **Efficient and effective management of tax revenues helps reduce dependency on external financing, enhance fiscal stability, and direct resources toward national priorities.**
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
    "🧾 4.2.1: Tax Revenue Collection",
    "🧾 4.2.2: Tax Administration Efficiency"
])

# === Tab 1: 4.2.1 ===
with tab1:
    st.markdown("### 🧾 4.2.1: Tax Revenue Collection")
    st.markdown("""
This subtopic examines the systems and processes in place for tax collection, focusing on reducing revenue leakages and improving enforcement.

#### Indicator 4.2.1.1: Tax Revenue as Percentage of GDP  
*_(Exact Indicator – Source: World Bank)_*

**Definition:**  
This indicator measures the total tax revenue collected as a proportion of the country's Gross Domestic Product (GDP). It reflects the overall capacity of the government to generate domestic revenue.
""")
    st.info("📊 Graph Placeholder: Tax Revenue (% of GDP)")

    st.markdown("""
#### Indicator 4.2.1.2: Taxpayer Base Expansion  
*_(Proxied by ATAF: Domestic Revenue from Large Taxpayers & Registered Taxpayers Data)_*

**Definition:**  
This indicator measures the growth rate in the number of registered taxpayers, reflecting the broadening of the tax base and improved tax compliance.  

**Proxy Justification:**  
The **ATAF indicator on Domestic Revenue from Large Taxpayers & Registered Taxpayers Data** provides an estimate of how the taxpayer base is expanding.
""")
    st.info("📊 Graph Placeholder: Registered Taxpayer Base Growth")

# === Tab 2: 4.2.2 ===
with tab2:
    st.markdown("### 🧾 4.2.2: Tax Administration Efficiency")
    st.markdown("""
This subtopic examines the systems and processes in place for tax collection, focusing on reducing revenue leakages and improving enforcement.

#### Indicator 4.2.2.1: Tax Collection Efficiency Score  
*_(Proxied by USAID/OECD: Tax Effort Ratio)_*

**Definition:**  
This indicator measures the ratio of actual tax revenue collected to the potential tax revenue that could be generated, assessing the efficiency of tax administration.  

**Proxy Justification:**  
The **USAID/OECD Tax Effort Ratio** measures how much tax is collected relative to the country’s tax capacity, making it a suitable proxy for tax collection efficiency.
""")
    st.info("📊 Graph Placeholder: Tax Effort Ratio (Collection Efficiency)")

    st.markdown("""
#### Indicator 4.2.2.2: Reduction in Tax Evasion  
*_(Proxied by USAID/OECD and ATAF: Tax Buoyancy)_*

**Definition:**  
This indicator measures the percentage decrease in estimated tax evasion rates, reflecting improvements in tax enforcement and compliance.  

**Proxy Justification:**  
The **Tax Buoyancy indicator from USAID/OECD and ATAF** measures how responsive tax revenue is to changes in GDP, indirectly capturing the effects of better enforcement in reducing tax evasion.
""")
    st.info("📊 Graph Placeholder: Tax Buoyancy (Evasion Reduction)")
