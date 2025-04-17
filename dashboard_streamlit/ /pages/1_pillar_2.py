import streamlit as st

# === Set Page Config ===
st.set_page_config(page_title="Pillar 2: Sustainable Finance", layout="wide")

# === Top-Level Framing ===
st.title("📌 Pillar 2: Sustainable Development Requires Sustainable Finance")
st.markdown("""
Sustainable development is not just about having goals—it's about having the **means** to achieve them.  
That’s where sustainable finance comes in.

To build resilient societies, governments need the ability to plan and invest over the long term, using **predictable**, **inclusive**, and **self-reliant** financial systems.  
Let’s break this down.
""")
st.divider()

# === Step 1: Understanding Sustainable vs. Unsustainable Finance ===
with st.expander("🔍 What is Sustainable vs. Unsustainable Finance?", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Sustainable Finance")
        st.markdown("""
Sustainable finance ensures long-term stability and growth by enabling countries to:
- Retain and create wealth.
- Minimize reliance on external, unpredictable funding.
- Invest responsibly in infrastructure, social services, and institutions.

**Key Characteristics:**
- **Endogenously Controlled**: Driven by domestic resource mobilization.  
- **Long-Term Orientation**: Policies aligned with national development plans.  
- **Predictable and Stable**: Reduces shocks to the economy.
        """)

    with col2:
        st.markdown("### ❌ Unsustainable Finance")
        st.markdown("""
Unsustainable finance prioritizes short-term fixes and leads to:
- Unstable budgets.
- Over-reliance on foreign aid or debt.
- Missed development goals.

**Key Characteristics:**
- **Short-Term Focus**: Reacting rather than planning.  
- **External Dependency**: Vulnerable to external shocks.  
- **Cost Mismatch**: Development costs exceed available revenues.
        """)

st.divider()

# === Step 2: Why It Matters for Africa ===
with st.expander("🌍 Why Sustainable Finance Matters for African Development", expanded=True):
    st.markdown("""
When African countries control and retain their wealth, they can:
- Invest in national priorities.
- Reduce inequality.
- Strengthen domestic economies.

**Key Aspects of Sustainable Finance in Africa:**
- **Wealth Retention**: Keeps capital in-country for reinvestment.  
- **Resource Management**: Ensures resources are used wisely.  
- **Inclusiveness**: Promotes equity and stability across society.
    """)
    st.success("Sustainable finance is a tool for **economic independence**, **resilience**, and **inclusive growth**.")

st.markdown("🔷 _Next, let’s explore how efficiency and effectiveness help us assess financial systems._")
st.divider()

# === Step 3: Entry Points and Framework ===
st.header("🧭 Entry Points: Efficiency and Effectiveness")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Entry Points to Assess Sustainable Finance")
    st.markdown("""
- **Efficiency**: Are resources being used wisely and with minimal waste?  
- **Effectiveness**: Are governments achieving their goals and delivering services?

These two lenses help us measure whether a country’s financial systems are:
- Aligned with long-term development.
- Resilient to shocks.
- Capable of inclusive service delivery.
    """)

with col2:
    st.markdown("### 📣 Why These Concepts Matter")
    st.markdown("""
Together, efficiency and effectiveness provide insights into whether a country is:
- Just spending… or building sustainably.  
- Reacting to crises… or investing in the future.
    """)
    st.info("In short: _Is the financial system working for the people and the planet?_")

# === Theme Navigation Section ===
st.markdown("""
### 🔽 Explore How We Measure These Ideas  
We break down this pillar into **five themes**. Each one focuses on a key piece of the puzzle. Click below to dive into each.
""")

theme_pages = {
    "💸 Theme 1: Public Debt Management Quality": "4_topic_4_2",
    "🏛️ Theme 2: Domestic Institutions’ Ability to Change a Country’s Position in R/GVCs": "5_topic_4_3",
    "🧭 Theme 3: Ownership Over Economic and Financial Flows": "6_topic_4_4",
    "🏦 Theme 4: DRM Institutions and Systems": "2_theme_4",
    "🤝 Theme 5: Derisking Strategies for Private Sector Engagement": "3_topic_4_1"
}

for label, page in theme_pages.items():
    st.page_link(f"pages/{page}.py", label=label, icon="📘")

st.divider()
st.caption("This page is part of the Nexus Dashboard | MVP Version 1.0")
