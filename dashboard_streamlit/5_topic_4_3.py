import streamlit as st
import pandas as pd
import pydeck as pdk

# === Set Page Config ===
st.set_page_config(page_title="Topic 4.3: Capital Markets", layout="wide")

# === Section Title & Overview ===
with st.container():
    st.title("📊 Topic 4.3: Capital Markets")
    st.markdown("""
    Capital markets are essential for mobilizing domestic financial resources and channeling savings into productive investments.  
    A well-developed capital market reduces reliance on foreign financing, supports sustainable economic growth, and strengthens financial stability.  
    **Effective management of capital markets ensures that resources are directed toward areas that maximize national development.**
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
    "📈 4.3.1: Market Capitalization",
    "🏦 4.3.2: Financial Intermediation",
    "💼 4.3.3: Institutional Investors"
])

# === Tab 1: Market Capitalization ===
with tab1:
    st.markdown("### 📈 4.3.1: Market Capitalization")

    st.markdown("""
This subtopic focuses on the size and activity of a country’s stock and bond markets, which reflect the ability of capital markets to raise funds for investment and development.

#### Indicator 4.3.1.1: Stock Market Capitalization to GDP  
**Definition:** Measures the total value of listed companies on the stock market as a percentage of GDP.  
**Relevance:**  
**Efficiency:** Indicates how well capital is being mobilized through the stock market relative to the economy’s size.  
**Effectiveness:** Demonstrates whether stock market growth translates into increased investment in key sectors.
    """)
    st.info("📊 Graph Placeholder: Stock Market Capitalization to GDP")

    st.markdown("""
#### Indicator 4.3.1.2: Bond Market Development  
**Definition:** Measures the volume of bonds issued and traded domestically.  
**Relevance:**  
**Efficiency:** Highlights the role of the bond market in efficiently raising long-term capital.  
**Effectiveness:** Assesses whether the funds raised are being directed toward infrastructure, social services, and other national priorities.
    """)
    st.info("📊 Graph Placeholder: Bond Market Development")

# === Tab 2: Financial Intermediation ===
with tab2:
    st.markdown("### 🏦 4.3.2: Financial Intermediation")

    st.markdown("""
This subtopic examines the systems and processes in place for tax collection, focusing on reducing revenue leakages and improving enforcement.

#### Indicator 4.3.2.1: Adequacy of International Reserves  
**Definition:** Measures the ratio of international reserves to short-term external debt.  
**Relevance:**  
**Efficiency:** Indicates how well reserves are managed to ensure financial stability.  
**Effectiveness:** Ensures reserves are sufficient to protect the economy against external shocks.
    """)
    st.info("📊 Graph Placeholder: Adequacy of International Reserves")

    st.markdown("""
#### Indicator 4.3.2.2: Banking Sector Development Index  
**Definition:** Measures the development and efficiency of the banking sector in terms of providing access to credit and mobilizing savings.  
**Relevance:**  
**Efficiency:** Reflects the ability of banks to allocate credit and manage deposits effectively.  
**Effectiveness:** Highlights whether banking sector improvements lead to economic growth and financial inclusion.
    """)
    st.info("📊 Graph Placeholder: Banking Sector Development Index")

# === Tab 3: Institutional Investors ===
with tab3:
    st.markdown("### 💼 4.3.3: Investment from Institutional Investors")

    st.markdown("""
This subtopic focuses on the role of institutional investors, such as pension funds and sovereign wealth funds, in contributing to long-term domestic development.

#### Indicator 4.3.3.1: Private Sector Credit to GDP  
**Definition:** Measures the total credit extended to the private sector as a percentage of GDP.  
**Relevance:**  
**Efficiency:** Demonstrates the role of financial institutions in providing credit efficiently to private entities.  
**Effectiveness:** Shows how credit expansion supports business growth and contributes to national development.
    """)
    st.info("📊 Graph Placeholder: Private Sector Credit to GDP")

    st.markdown("""
#### Indicator 4.3.3.2: Pension Funds and Sovereign Wealth Funds Investments  
**Definition:** Measures the proportion of assets from these funds invested in domestic capital markets.  
**Relevance:**  
**Efficiency:** Tracks how well institutional investments are directed toward productive domestic sectors.  
**Effectiveness:** Evaluates whether these investments contribute to sustainable and inclusive growth.
    """)
    st.info("📊 Graph Placeholder: Pension and SWF Investments")
