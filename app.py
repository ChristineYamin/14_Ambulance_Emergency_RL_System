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

#----------------------------------------
# CSS
#----------------------------------------
def load_css():
    return """
    <style>
    /* 1. Base Dark Theme */
    [data-testid="stAppViewContainer"], [data-testid="stSidebar"], [data-testid="stHeader"] {
        background-color: #0E1117 !important;
        color: #E0E0E0 !important;
    }

    /* 2. Text Elements */
    h1, h2, h3, p { color: #FFFFFF !important; }
    h2 { color: #00E5FF !important; } /* Accent color for headers */

    /* 3. Metric Cards */
    div[data-testid="metric-container"] {
        background: #161B22 !important; /* Slightly lighter than background */
        border-radius: 12px !important;
        padding: 20px !important;
        border: 1px solid #30363D !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3) !important;
    }

    /* 4. Sidebar Button */
    div.stButton > button {
        background-color: #00E5FF !important;
        color: #0E1117 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
    }

    /* 5. Tables - Making them 'Professional' */
    [data-testid="stDataFrame"] {
        border: 1px solid #00E5FF !important;
    }

    /* This targets the column headers of the dataframe */
    [data-testid="stDataFrame"] div[role="columnheader"] {
        background-color: #1F2937 !important;
        color: #00E5FF !important;
        border-bottom: 2px solid #00E5FF !important;
    }

    /* Target dataframe cells for consistent text color */
    [data-testid="stDataFrame"] td {
        color: #E0E0E0 !important;
        background-color: #161B22 !important;
    }
    </style>

   
    """

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
# Set the style to dark
plt.style.use('dark_background')

fig, ax = plt.subplots(
    figsize=(10, 4)
)

# Transparent background for the figure and axes
fig.patch.set_facecolor('#0E1117')
ax.set_facecolor('#1F2937')

ax.plot(
    history_df["Generation"],
    history_df["Score"],
    color="#00E5FF",
    linewidth=3
)

# Style titles and labels
ax.set_title("Fitness Score Across Generations", color='white')
ax.set_xlabel("Generation", color='white')
ax.set_ylabel("Predicted Travel Time", color='white')

# Adjust tick colors
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

# Remove borders (spines) for a cleaner "app" look
for spine in ax.spines.values():
    spine.set_edgecolor('#00E5FF')

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
# Upgraded Interactive Route Map
# -----------------------------------

st.subheader("🗺️ Optimized Delivery Route Map")

center_lat = merged["Latitude"].mean()
center_lon = merged["Longitude"].mean()

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=11,
    tiles="CartoDB dark_matter"
)

route_points = list(
    zip(
        merged["Latitude"],
        merged["Longitude"]
    )
)

# Draw optimized route line
folium.PolyLine(
    route_points,
    color="#00E5FF",
    weight=5,
    opacity=0.9,
    tooltip="Optimized Delivery Route"
).add_to(m)

# Add numbered markers
for idx, row in merged.iterrows():

    location_name = row["Location"]
    stop_number = idx + 1

    # Hospital = green
    if "Central_Hospital" in location_name:
        marker_color = "#22C55E"
        icon_symbol = "🏥"

    # Last clinic before returning = red
    elif idx == len(merged) - 2:
        marker_color = "#EF4444"
        icon_symbol = "📦"

    # Normal clinics = blue
    else:
        marker_color = "#2563EB"
        icon_symbol = "📦"

    html_marker = f"""
    <div style="
        background-color:{marker_color};
        color:white;
        border-radius:50%;
        width:34px;
        height:34px;
        text-align:center;
        line-height:34px;
        font-weight:bold;
        font-size:14px;
        border:2px solid white;
        box-shadow:0px 0px 8px rgba(255,255,255,0.6);
    ">
        {stop_number}
    </div>
    """

    popup_text = f"""
    <b>Stop {stop_number}</b><br>
    {icon_symbol} {location_name}
    """

    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=popup_text,
        tooltip=f"Stop {stop_number}: {location_name}",
        icon=folium.DivIcon(
            html=html_marker
        )
    ).add_to(m)

# Add start/end label
start_row = merged.iloc[0]

folium.Marker(
    location=[
        start_row["Latitude"],
        start_row["Longitude"]
    ],
    popup="🏥 Central Hospital: Start / End Point",
    tooltip="Central Hospital",
    icon=folium.Icon(
        color="green",
        icon="plus-sign"
    )
).add_to(m)

st_folium(
    m,
    width=1200,
    height=650
)

st.markdown("""
### 🧭 Map Legend

🟢 **Green** = Central Hospital / Start & End Point  
🔵 **Blue** = Clinic Delivery Stops  
🔴 **Red** = Final Clinic Before Returning  
🟦 **Cyan Line** = Optimized Delivery Route
""")


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