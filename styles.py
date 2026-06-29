def load_css():
    return """
    <style>
    /* Target the main app view container */
    [data-testid="stAppViewContainer"] {
        background-color: #0E1117 !important;
    }

    h1, h2, h3 {
        color: white !important;
    }

    h2 {
        color: #00E5FF !important;
    }

    /* Target metrics container */
    div[data-testid="metric-container"] {
        background-color: #1F2937 !important;
        border-radius: 18px !important;
        padding: 18px !important;
        border: 1px solid #00E5FF !important;
        box-shadow: 0px 0px 12px rgba(0,229,255,0.25) !important;
    }

    div[data-testid="metric-container"] label {
        color: white !important;
        font-size: 17px !important;
    }

    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #00E5FF !important;
        font-size: 30px !important;
        font-weight: bold !important;
    }
    </style>
    """