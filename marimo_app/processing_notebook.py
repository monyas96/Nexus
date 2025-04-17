import marimo as mo
import pandas as pd

app = mo.App()

# === Load Data ===
# Set correct paths relative to project root
OBT_PATH = "outputs/master_obt.csv"
EXPORT_DIR = "outputs"
df = pd.read_csv(OBT_PATH)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# === UI Widgets ===

# Dropdown: Select Nexus Code
options = sorted(df["nexus_code"].dropna().unique())
nexus_dropdown = mo.ui.dropdown(
    options=options,
    label="Select Nexus Code",
    value=options[0]  # always picks a valid one
)


# Slider: Filter by Year
year_slider = mo.ui.slider(
    label="Filter by Year",
    start=2000,
    stop=2022,
    step=1,
    value=2020
)
year_slider

# === Filter Data ===
filtered_df = df[
    (df["nexus_code"] == nexus_dropdown.value) &
    (df['year'] == year_slider.value)
]

filtered_df.head()

# === Optional: Export Filtered Data ===
EXPORT_PATH = f"outputs/{nexus_dropdown.value}_filtered.csv"
filtered_df.to_csv(EXPORT_PATH, index=False)

mo.md(f"✅ Exported to `{EXPORT_PATH}`")
