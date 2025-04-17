import streamlit as st
import pandas as pd
import pydeck as pdk

# === Set Page Config ===
st.set_page_config(page_title="Topic 4.4: Illicit Financial Flows", layout="wide")

# === Section Title & Overview ===
with st.container():
    st.title("💸 Topic 4.4: Illicit Financial Flows (IFFs)")
    st.markdown("""
    Illicit financial flows (IFFs) are a critical challenge for domestic resource mobilization as they represent a significant loss of financial resources that could otherwise be used for development.  
    IFFs include practices like trade mispricing, tax evasion, corruption, and criminal activities. Addressing IFFs is essential to ensure that financial resources remain within the country and are directed toward development priorities.
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

tab1, tab2, tab3 = st.tabs([
    "📉 4.4.1: Magnitude of Illicit Financial Flows",
    "🔍 4.4.2: Types of IFFs",
    "🛡️ 4.4.3: Detection and Enforcement"
])

# === Tab 1: Magnitude of IFFs ===
with tab1:
    st.markdown("### 📉 4.4.1: Magnitude of Illicit Financial Flows")
    st.markdown("""
This subtopic assesses the scale and impact of IFFs on a country’s economy, highlighting areas where revenue is being lost.

#### Indicator 4.4.1.1: IFFs as a Percentage of GDP  
_(Proxied by Global Financial Integrity: Estimated Value of Illicit Financial Flows as a Proportion of GDP)_

**Definition:**  
This indicator measures the estimated value of illicit financial flows as a share of a country’s Gross Domestic Product (GDP), reflecting the extent to which illicit capital flight affects economic stability.

**Proxy Justification:**  
Data from **Global Financial Integrity (GFI)** estimates IFFs as a percentage of GDP based on trade discrepancies, unrecorded capital movements, and other financial anomalies.
    """)
    st.info("📊 Graph Placeholder: IFFs as a Percentage of GDP")

    st.markdown("""
#### Indicator 4.4.1.2: Annual IFF Volume  
_(Proxied by Global Financial Integrity: Total Volume of Illicit Financial Flows Annually)_

**Definition:**  
This indicator quantifies the total estimated volume of illicit financial flows in absolute terms (e.g., USD billions per year), providing insight into the scale of illegal capital movement.

**Proxy Justification:**  
**Global Financial Integrity (GFI)** provides annual estimates of illicit flows based on anomalies in trade data, cross-border capital flight, and financial misreporting.
    """)
    st.info("📊 Graph Placeholder: Annual IFF Volume")

# === Tab 2: Types of IFFs ===
with tab2:
    st.markdown("### 🔍 4.4.2: Types of Illicit Financial Flows")

    st.markdown("""
This subtopic categorizes and measures specific sources of IFFs, such as trade mispricing and criminal activities.

#### Indicator 4.4.2.1: Trade Mispricing  
_(Proxied by Global Financial Integrity: Trade Value Gaps in International Trade Data)_

**Definition:**  
Trade mispricing occurs when importers or exporters deliberately misstate the price, quantity, or quality of goods and services to shift capital across borders illegally.

**Proxy Justification:**  
The trade value gap estimates from Global Financial Integrity provide an approximate measure of trade mispricing by analyzing mismatches in reported trade data.
    """)
    st.info("📊 Graph Placeholder: Trade Mispricing")

    st.markdown("""
#### Indicator 4.4.2.2: Tax Evasion  
_(Proxied by IMF: Taxpayer Registration Data)_

**Definition:**  
Refers to illegal practices to avoid paying taxes, including underreporting income, inflating deductions, and hiding money in offshore accounts.

**Proxy Justification:**  
IMF’s taxpayer registration indicators, such as the percentage of registered taxpayers relative to the labor force, provide insight into tax compliance trends.
    """)
    st.info("📊 Graph Placeholder: Tax Evasion")

    st.markdown("""
#### Indicator 4.4.2.3: Criminal Activities  
_(Proxied by UNODC: Criminal Activity Data)_

**Definition:**  
This indicator tracks illicit financial flows generated from organized crime, drug trafficking, human trafficking, and other illegal activities.

**Proxy Justification:**  
The UNODC dataset provides estimates of financial flows associated with criminal activities, offering insights into the illicit scale of IFFs from organized crime.
    """)
    st.info("📊 Graph Placeholder: Criminal Activities")

# === Tab 3: Detection and Enforcement ===
with tab3:
    st.markdown("### 🛡️ 4.4.3: Detection and Enforcement")

    st.markdown("""
This subtopic focuses on the ability of tax and customs authorities to detect and prevent IFFs effectively.

#### Indicator 4.4.3.1: Effectiveness of Anti-IFF Measures  
_(Proxied by World Justice Project & CPIA Transparency Ratings)_

**Definition:**  
This indicator measures the number of successful prosecutions and enforcement actions taken against IFF-related offenses.

**Proxy Justification:**  
The World Justice Project’s Rule of Law Index and CPIA transparency ratings provide a broad measure of governance quality and enforcement strength.
    """)
    st.info("📊 Graph Placeholder: Anti-IFF Measures")

    st.markdown("""
#### Indicator 4.4.3.2: Corruption and Bribery  
_(Proxied by WJP Rule of Law Index & WB Governance Indicators)_

**Definition:**  
This indicator measures the extent of corruption and bribery in both public and private sectors, where illicit payments distort economic and governance structures.

**Proxy Justification:**  
The World Justice Project (WJP) Rule of Law Index and World Bank Governance Indicators provide relevant metrics, including the "Control of Corruption" score and public perceptions of bribery prevalence.
    """)
    st.info("📊 Graph Placeholder: Corruption and Bribery")
