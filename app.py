import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Emergency Medical Supply Optimization",
    page_icon="🚑",
    layout="wide"
)

# -----------------------------------
# CSS: Professional Dark Navy Theme
# -----------------------------------

def load_css():
    return """
    <style>

    /* Main background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #071A2F 0%, #0B2447 55%, #112D4E 100%);
        color: #E5E7EB;
    }

    [data-testid="stHeader"] {
        background-color: rgba(7, 26, 47, 0);
    }

    /* Hide default Streamlit footer */
    footer {
        visibility: hidden;
    }

    /* Headings */
    h1, h2, h3, p {
        color: #F8FAFC !important;
    }

    h2 {
        color: #38BDF8 !important;
    }

    /* Hero section */
    .hero-card {
        background: linear-gradient(135deg, #0B2447 0%, #112D4E 100%);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 22px;
        padding: 28px 34px;
        margin-bottom: 18px;
        box-shadow: 0px 8px 28px rgba(0, 0, 0, 0.35);
    }

    .hero-title {
        font-size: 38px;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #CBD5E1;
        margin-bottom: 0px;
    }

    .status-pill {
        display: inline-block;
        background-color: rgba(34, 197, 94, 0.15);
        color: #22C55E;
        border: 1px solid rgba(34, 197, 94, 0.45);
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 700;
        margin-top: 14px;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: rgba(11, 36, 71, 0.92) !important;
        border-radius: 18px !important;
        padding: 20px !important;
        border: 1px solid rgba(56, 189, 248, 0.28) !important;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.28) !important;
    }

    div[data-testid="metric-container"] label {
        color: #CBD5E1 !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }

    div[data-testid="metric-container"] div {
        color: #38BDF8 !important;
        font-size: 28px !important;
        font-weight: 800 !important;
    }

    /* Custom cards */
    .info-card {
        background: rgba(11, 36, 71, 0.95);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.25);
    }

    .card-title {
        color: #38BDF8;
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .card-text {
        color: #E2E8F0;
        font-size: 15px;
        line-height: 1.6;
    }

    .route-box {
        background: rgba(17, 45, 78, 0.95);
        border-left: 4px solid #38BDF8;
        padding: 16px;
        border-radius: 12px;
        color: #E2E8F0;
        font-size: 15px;
        line-height: 1.7;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        border-radius: 14px !important;
    }

    /* Download button */
    div.stDownloadButton > button {
        background-color: #38BDF8 !important;
        color: #071A2F !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 18px !important;
    }

    </style>
    """

st.markdown(load_css(), unsafe_allow_html=True)

# -----------------------------------
# Load Data
# -----------------------------------

route_df = pd.read_csv("notebooks/optimized_supply_route.csv")
history_df = pd.read_csv("notebooks/fitness_history.csv")
locations_df = pd.read_csv("notebooks/locations.csv")

# -----------------------------------
# Core Metrics
# -----------------------------------

initial_score = history_df["Score"].iloc[0]
best_score = history_df["Score"].min()
improvement = ((initial_score - best_score) / initial_score) * 100

clinic_count = len(route_df) - 2
total_stops = len(route_df) - 1
generation_count = len(history_df)

# -----------------------------------
# Hero Section
# -----------------------------------

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">🚑 Emergency Medical Supply Distribution Optimization</div>
        <div class="hero-subtitle">
            AI-powered delivery route optimization using XGBoost travel-time prediction and Genetic Algorithm search.
        </div>
        <div class="status-pill">🟢 SYSTEM STATUS : ONLINE</div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# KPI Section
# -----------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("🏥 Hospital", "1")
col2.metric("📦 Clinics", clinic_count)
col3.metric("⏱ Best Time", f"{best_score:.2f} min")
col4.metric("⚡ Improvement", f"{improvement:.2f}%")
col5.metric("🧬 Generations", generation_count)

# -----------------------------------
# Merge Route with Coordinates
# -----------------------------------

merged = route_df.merge(
    locations_df,
    on="Location",
    how="left"
)

# -----------------------------------
# Main Dashboard Layout: Map + Recommendation
# -----------------------------------

left_col, right_col = st.columns([1.6, 1])

with left_col:

    st.subheader("🗺️ Optimized Route Map")

    center_lat = merged["Latitude"].mean()
    center_lon = merged["Longitude"].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        tiles="OpenStreetMap",
        width="100%",
        height="100%"
    )

    route_points = list(
        zip(
            merged["Latitude"],
            merged["Longitude"]
        )
    )

    folium.PolyLine(
        route_points,
        color="#2563EB",
        weight=3,
        opacity=0.75,
        tooltip="Optimized Delivery Sequence"
    ).add_to(m)

    for idx, row in merged.iterrows():

        location_name = row["Location"]

        # Skip final hospital marker because it overlaps with the start
        if location_name == "Central_Hospital" and idx == len(merged) - 1:
            continue

        if location_name == "Central_Hospital":
            marker_color = "#22C55E"
            display_number = f"1/{len(merged)}"
            icon_symbol = "🏥"

        elif idx == len(merged) - 2:
            marker_color = "#EF4444"
            display_number = str(idx + 1)
            icon_symbol = "📦"

        else:
            marker_color = "#2563EB"
            display_number = str(idx + 1)
            icon_symbol = "📦"

        html_marker = f"""
        <div style="
            background-color:{marker_color};
            color:white;
            border-radius:50%;
            width:30px;
            height:30px;
            text-align:center;
            line-height:30px;
            font-weight:bold;
            font-size:12px;
            border:2px solid white;
            box-shadow:0px 0px 5px rgba(0,0,0,0.5);
        ">
            {display_number}
        </div>
        """

        popup_text = f"""
        <b>Stop {display_number}</b><br>
        {icon_symbol} {location_name}
        """

        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=popup_text,
            tooltip=f"Stop {display_number}: {location_name}",
            icon=folium.DivIcon(html=html_marker)
        ).add_to(m)

    st_folium(
        m,
        use_container_width=True,
        height=530
    )

    st.caption(
        "Note: The map visualizes the optimized stop sequence. "
        "The route line connects delivery stops and does not represent turn-by-turn road navigation."
    )

with right_col:

    st.subheader("🧠 AI Recommendation")

    st.markdown(
        f"""
        <div class="info-card">
            <div class="card-title">Recommended Delivery Plan</div>
            <div class="card-text">
                The system recommends dispatching emergency medical supplies from 
                <b>Central_Hospital</b>, visiting all assigned clinics, and returning to 
                <b>Central_Hospital</b>.
                <br><br>
                The Genetic Algorithm reduced predicted delivery time from 
                <b>{initial_score:.2f} minutes</b> to 
                <b>{best_score:.2f} minutes</b>.
                <br><br>
                Estimated improvement: <b>{improvement:.2f}%</b>.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("⚡ Before vs After")

    before_col, after_col = st.columns(2)

    before_col.metric(
        "Before",
        f"{initial_score:.2f} min"
    )

    after_col.metric(
        "After",
        f"{best_score:.2f} min"
    )

    st.subheader("🚚 Route Sequence")

    route_text = " → ".join(route_df["Location"].tolist())

    st.markdown(
        f"""
        <div class="route-box">
            {route_text}
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------------
# Performance Chart + Route Table
# -----------------------------------

st.subheader("📈 Optimization Performance & Delivery Plan")

chart_col, table_col = st.columns([1, 1.25])

with chart_col:

    st.markdown(
        """
        <div class="info-card">
            <div class="card-title">Genetic Algorithm Performance</div>
            <div class="card-text">
                Fitness score decreases as the Genetic Algorithm searches for a better delivery sequence.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    plt.style.use("dark_background")

    fig, ax = plt.subplots(figsize=(5.5, 2.8))

    fig.patch.set_facecolor("#071A2F")
    ax.set_facecolor("#0B2447")

    ax.plot(
        history_df["Generation"],
        history_df["Score"],
        color="#38BDF8",
        linewidth=2.5
    )

    ax.axhline(
        best_score,
        color="#22C55E",
        linestyle="--",
        linewidth=1.8
    )

    ax.set_title(
        "Fitness Score Across Generations",
        color="white",
        fontsize=10
    )

    ax.set_xlabel(
        "Generation",
        color="white",
        fontsize=8
    )

    ax.set_ylabel(
        "Travel Time",
        color="white",
        fontsize=8
    )

    ax.tick_params(
        axis="x",
        colors="white",
        labelsize=7
    )

    ax.tick_params(
        axis="y",
        colors="white",
        labelsize=7
    )

    for spine in ax.spines.values():
        spine.set_edgecolor("#38BDF8")

    ax.grid(
        alpha=0.18
    )

    st.pyplot(
        fig,
        use_container_width=True
    )

with table_col:

    st.markdown(
        """
        <div class="table-card">
            <div class="card-title">📦 Optimized Delivery Route</div>
        """,
        unsafe_allow_html=True
    )

    table_html = route_df.to_html(
        index=False,
        classes="custom-route-table",
        border=0
    )

    st.markdown(
        table_html,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True
    )
# -----------------------------------
# Best Route Details
# -----------------------------------

st.subheader("🏆 Best Route Statistics")

stat_col1, stat_col2, stat_col3 = st.columns(3)

stat_col1.metric(
    "Best Predicted Travel Time",
    f"{best_score:.2f} min"
)

stat_col2.metric(
    "Number of Stops",
    total_stops
)

stat_col3.metric(
    "Clinics Served",
    clinic_count
)

# -----------------------------------
# Download Result
# -----------------------------------

st.subheader("⬇ Download Result")

st.download_button(
    label="Download Optimized Route CSV",
    data=route_df.to_csv(index=False),
    file_name="optimized_supply_route.csv",
    mime="text/csv"
)

# -----------------------------------
# About Project
# -----------------------------------

with st.expander("📖 About This Project"):

    st.markdown("""
    ### Project Purpose

    This project optimizes emergency medical supply distribution from a central hospital to multiple clinics.

    ### AI Pipeline

    1. **XGBoost Regressor** predicts travel time between medical locations.
    2. **Genetic Algorithm** searches for the best delivery sequence.
    3. **Streamlit Dashboard** visualizes the optimized route, predicted travel time, and route performance.

    ### Map Note

    The route line shows the optimized stop sequence. It does not represent turn-by-turn road navigation.
    """)

# -----------------------------------
# Footer
# -----------------------------------

st.success("Optimization Completed Successfully ✅")