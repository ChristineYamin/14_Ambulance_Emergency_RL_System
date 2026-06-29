import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium

from streamlit_folium import st_folium
from styles import load_css
# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Emergency Medical Supply Optimization",
    page_icon="🚑",
    layout="wide"
)

# CSS
st.markdown(load_css(), unsafe_allow_html=True)

# -----------------------------------
# Load Data
# -----------------------------------

route_df = pd.read_csv(
    "notebooks/optimized_supply_route.csv"
)

history_df = pd.read_csv(
    "notebooks/fitness_history.csv"
)

locations_df = pd.read_csv(
    "notebooks/locations.csv"
)

# -----------------------------------
# Title
# -----------------------------------

st.title(
    "🚑 Emergency Medical Supply Distribution Optimization"
)

st.markdown("""
This system uses:

- 🤖 XGBoost Machine Learning
- 🧬 Genetic Algorithm Optimization
- 🗺️ Route Visualization

to find the most efficient medical supply delivery route.
""")

st.success(
    "🟢 SYSTEM STATUS : ONLINE"
)

#------------------------------------
# Side Bar
#-----------------------------------
st.sidebar.title("Simulation Settings")
population = st.sidebar.slider(
    "Population Size",
    100,
    500,
    300
)

generations = st.sidebar.slider(
    "Generations",
    20,
    300,
    100
)

pickup_hour = st.sidebar.slider(
    "Pickup Hour",
    0,
    23,
    10
)
run = st.sidebar.button("🚀 Run Optimization")
# -----------------------------------
# KPI Section
# -----------------------------------

st.subheader("📊 Optimization Summary")

col1,col2,col3,col4,col5=st.columns(5)

col1.metric(
    "🚑 Hospital",
    "1"
)

col2.metric(
    "📦 Clinics",
    len(route_df)-2
)

col3.metric(
    "⏱ Travel Time",
    f"{history_df.Score.min():.2f} min"
)

col4.metric(
    "🧬 Generations",
    len(history_df)
)

col5.metric(
    "🚚 Stops",
    len(route_df)-1
)

# -----------------------------------
# Route Table
# -----------------------------------

st.subheader("📦 Optimized Delivery Route")

st.dataframe(
    route_df,
    use_container_width=True
)

# -----------------------------------
# Route Sequence
# -----------------------------------

st.subheader("🚚 Route Sequence")

route_text = " → ".join(
    route_df["Location"].tolist()
)

st.info(route_text)

# -----------------------------------
# Fitness Chart
# -----------------------------------

st.subheader("📈 Genetic Algorithm Performance")

fig, ax = plt.subplots(
    figsize=(10, 4)
)

ax.plot(
    history_df["Generation"],
    history_df["Score"],
    linewidth=3
)

ax.set_title(
    "Fitness Score Across Generations"
)

ax.set_xlabel(
    "Generation"
)

ax.set_ylabel(
    "Predicted Travel Time"
)

st.pyplot(fig)

# -----------------------------------
# Merge Route with Coordinates
# -----------------------------------

merged = route_df.merge(
    locations_df,
    on="Location",
    how="left"
)

# -----------------------------------
# Map
# -----------------------------------

st.subheader("🗺️ Optimized Route Map")

center_lat = merged["Latitude"].mean()
center_lon = merged["Longitude"].mean()

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=11
)

# Route markers

for idx, row in merged.iterrows():

    popup_text = (
        f"Stop {idx+1}<br>"
        f"{row['Location']}"
    )

    folium.Marker(
        [row["Latitude"], row["Longitude"]],
        popup=popup_text,
        tooltip=row["Location"]
    ).add_to(m)

# Route line

route_points = list(
    zip(
        merged["Latitude"],
        merged["Longitude"]
    )
)

folium.PolyLine(
    route_points,
    weight=5
).add_to(m)

st_folium(
    m,
    width=1200,
    height=600
)

# -----------------------------------
# Best Route Details
# -----------------------------------

st.subheader("🏆 Best Route Statistics")

st.write(
    f"Best Predicted Travel Time: "
    f"**{history_df['Score'].min():.2f} minutes**"
)

st.write(
    f"Number of Stops: "
    f"**{len(route_df)-1}**"
)

# -----------------------------------
# Footer
# -----------------------------------

st.success(
    "Optimization Completed Successfully ✅"
)