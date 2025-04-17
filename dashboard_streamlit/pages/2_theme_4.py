import streamlit as st

st.set_page_config(page_title="Theme 4: Domestic Resource Mobilization", layout="wide")

# === Title ===
st.title("📁 Theme 4: Domestic Resource Mobilization (DRM) – Institutions & Systems")

# === Rationale Section ===
with st.container():
    st.subheader("Rationale:")
    st.markdown("""
    **What:** Countries have money, but it is not where it should be, it is not used as it should be, and does not benefit whom it should.

    **Why:** Institutional weaknesses in managing and capturing domestic financial resources.

    **Therefore:** Stronger ability to evaluate and manage domestic resources contributes to offering sustainable financial resources.
    """, unsafe_allow_html=True)

# === Instruction ==
st.info("💡 The DRM system is structured around four critical topics. Click on any of the buttons below to explore subtopics and indicators assessing efficiency and effectiveness.")

st.divider()

# === Topics Grid ===
col1, col2 = st.columns(2)

# === Topic 4.1 ===
with col1:
    st.page_link("pages/3_topic_4_1.py", label="💸 Topic 4.1: Public Expenditures")
    st.markdown("""
    > Efficient management of public funds ensures that they are allocated toward priority sectors like education and infrastructure and are spent responsibly to avoid waste.
    """)

# === Topic 4.3 ===
with col2:
    st.page_link("pages/5_topic_4_3.py", label="📈 Topic 4.3: Capital Markets")
    st.markdown("""
    > Well-developed capital markets channel savings into productive investments, promoting economic growth and reducing reliance on foreign financing.
    """)

# === Topic 4.2 ===
with col1:
    st.page_link("pages/4_topic_4_2.py", label="🧾 Topic 4.2: Budget and Tax Revenues")
    st.markdown("""
    > Strengthening tax administration and expanding the taxpayer base are critical for mobilizing domestic resources while minimizing revenue losses from inefficiencies.
    """)

# === Topic 4.4 ===
with col2:
    st.page_link("pages/6_topic_4_4.py", label="🚫💰 Topic 4.4: Illicit Financial Flows (IFFs)")
    st.markdown("""
    > Addressing IFFs helps retain domestic resources by curbing trade mispricing, tax evasion, and corruption, ensuring that financial resources stay within the country.
    """)

st.divider()
st.caption("Theme 4 supports countries in strengthening domestic financial management systems for long-term, inclusive development.")
