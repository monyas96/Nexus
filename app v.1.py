# app.py

import streamlit as st
import os

# === Set config 
st.set_page_config(page_title="Nexus Dashboard", layout="wide")

# === Define Pages ===
pillar_2_page = st.Page(
    "pages/1_pillar_2.py",
    title="📌 Pillar 2: Sustainable Financing",
    icon="💰",
    url_path="pillar-2"
)

theme_4_pages = [
    st.Page("pages/2_theme_4.py", title="📁 Theme 4: DRM Institutions", icon="📁"),
    st.Page("pages/3_topic_4_1.py", title="📘 Topic 4.1: Public Expenditures"),
    st.Page("pages/4_topic_4_2.py", title="📘 Topic 4.2: Budget and Tax Revenues"),
    st.Page("pages/5_topic_4_3.py", title="📘 Topic 4.3: Capital Markets"),
    st.Page("pages/6_topic_4_4.py", title="📘 Topic 4.4: Illicit Financial Flows"),
]

# === Navigation ===
st.navigation(
    {
        "🏠 Nexus Dashboard": [
            st.Page("app.py", title="🏠 Home", default=True)
        ],
        "📊 Data": [
            pillar_2_page,
            *theme_4_pages
        ]
    },
    position="sidebar",
    expanded=True
)

# === Top logo row ===
image_dir = "Dashboard images"  # Use relative path from app.py location

col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    st.image(os.path.join(image_dir, "OSAA identifier color.png"), width=200)
with col3:
    st.image(os.path.join(image_dir, "quintet-logo-en-e1702486213916-1024x428.webp"), width=120)

# === Home Content ===
st.title("Data-Driven Tool for Development Nexus Thinking")
st.markdown("**MVP - Version 1.0**")
st.warning("This version is for validation purposes only, and the data presented is under review to ensure accuracy and quality.")

st.markdown("""
This dashboard highlights the nexus approach to development, demonstrating the interplay between peace, sustainable financing, and strong institutions.

- 🔍 **Data Insights**: Interactive visualization of trends  
- 📊 **Analytics**: Breakdowns by themes and geographies  
- 🌍 **Impact**: Connecting policy and real-world changes
""")
st.divider()

# === Pillar Summaries ===
st.header("🔎 Explore the Four Pillars")

with st.expander("📌 Pillar 1: Durable Peace Requires Sustainable Development"):
    st.markdown("""
    Lasting peace cannot exist without a foundation of sustainable development.  
    This pillar focuses on how economic growth, climate adaptation, resilience, and social equity  
    collectively contribute to stable and peaceful societies.
    """)
    st.info("🚧 Coming Soon")

with st.expander("📌 Pillar 2: Sustainable Development Requires Sustainable Financing"):
    st.markdown("""
    Sustainable development needs financing that is substantial, enduring, and resilient.  
    This pillar examines how countries secure nationally owned, long-term financing aligned with local priorities.
    """)
    st.page_link(pillar_2_page, label="👉 Go to Pillar 2", icon="💰")

with st.expander("📌 Pillar 3: Sustainable Financing Requires Control Over Economic and Financial Flows"):
    st.markdown("""
    Achieving sustainable financing requires African states to have sovereignty over their economic and financial resources.  
    This pillar highlights the ability to manage and direct flows effectively toward national development goals.
    """)
    st.info("🚧 Coming Soon")

with st.expander("📌 Pillar 4: Control Over Economic and Financial Flows Requires Strong Institutions"):
    st.markdown("""
    Managing economic and financial flows depends on strong, effective, and transparent institutions.  
    This pillar focuses on the country systems and capacities needed to regulate, implement, and ensure accountability.
    """)
    st.info("🚧 Coming Soon")
