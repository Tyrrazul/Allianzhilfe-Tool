import streamlit as st
import math
import pandas as pd
import plotly.express as px

# Hintergrund & Göttersymbole anzeigen
def set_custom_background_and_icons():
    background_url = "https://raw.githubusercontent.com/Tyrrazul/Allianzhilfe-Tool/main/Papyrus%20background.png"
    khorne_url = "https://raw.githubusercontent.com/Tyrrazul/Allianzhilfe-Tool/main/khorne.png"
    nurgle_url = "https://raw.githubusercontent.com/Tyrrazul/Allianzhilfe-Tool/main/nurgle.png"
    slaanesh_url = "https://raw.githubusercontent.com/Tyrrazul/Allianzhilfe-Tool/main/slaanesh.png"
    tzeentch_url = "https://raw.githubusercontent.com/Tyrrazul/Allianzhilfe-Tool/main/tzeentch.png"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=UnifrakturCook:wght@700&display=swap');

    .stApp {{
        font-family: 'UnifrakturCook', cursive;
        background-color: #1a1a1a;
        color: #e6e2dc;
        min-height: 100vh;
        margin: 0;
        padding: 1rem 2rem;
    }}

    h1, h2, h3, h4 {{
        color: #b30000;
        text-shadow: 1.5px 1.5px 3px #000;
        font-weight: 700;
    }}

    .stButton>button {{
        background-color: #550000;
        color: #f0e6dc;
        border: 2px solid #a00000;
        border-radius: 8px;
        font-weight: 700;
        padding: 0.5em 1.2em;
        box-shadow: 2px 2px 8px #000;
        transition: 0.2s ease-in-out;
        font-family: 'UnifrakturCook', cursive;
        font-size: 1.1rem;
        cursor: pointer;
    }}
    .stButton>button:hover {{
        background-color: #770000;
        transform: scale(1.05);
        box-shadow: 3px 3px 12px #330000;
    }}

    .corner-icon {{
        position: fixed;
        width: 240px;
        height: 240px;
        z-index: 999;
    }}

    #slaanesh {{ top: 10px; left: 10px; }}
    #nurgle {{ top: 10px; right: 10px; }}
    #khorne {{ bottom: 10px; left: 10px; }}
    #tzeentch {{ bottom: 10px; right: 10px; }}
    </style>

    <img src="{slaanesh_url}" class="corner-icon" id="slaanesh">
    <img src="{nurgle_url}" class="corner-icon" id="nurgle">
    <img src="{khorne_url}" class="corner-icon" id="khorne">
    <img src="{tzeentch_url}" class="corner-icon" id="tzeentch">
    """, unsafe_allow_html=True)

set_custom_background_and_icons()

# Mindesthilfezeit basierend auf Ziel-Level und Typ
def get_min_help_seconds(target_level, help_type):
    help_table = {
        "Gebäude": {
            (1, 6): 60,
            (7, 7): 180,
            (8, 8): 300,
            (9, 11): 600,
            (12, 14): 1200,
            (15, 15): 2400,
            (16, 18): 3600,
            (19, 20): 5400,
            (21, 30): 7200
        },
        "Ritual": {
            1: 60,
            2: 180,
            3: 300,
            4: 600,
            5: 1200,
            6: 2400,
            7: 3600,
            8: 5400,
            9: 7200,
            10: 14400
        }
    }
    if help_type == "Gebäude":
        for level_range, seconds in help_table["Gebäude"].items():
            if level_range[0] <= target_level <= level_range[1]:
                return seconds
    else:  # Ritual
        return help_table["Ritual"].get(target_level, 60)
    return 60

def seconds_to_h_m_s(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h}h {m}m {s}s"

st.set_page_config(page_title="Allianzhilfe-Rechner", layout="centered")
st.title("Warhammer: Chaos & Conquest - Allianzhilfe-Rechner")

st.markdown("""
Berechne, wie viel Zeit du bei **Gebäuden** oder **Ritualen** durch Allianzhilfe einsparst.
""")

help_type = st.selectbox("Was möchtest du berechnen?", ["Gebäude", "Ritual"])

col1, col2 = st.columns(2)

with col1:
    hours = st.number_input("Startzeit - Stunden", min_value=0, max_value=999, value=1)
    helps = st.number_input("Freigeschaltete Allianzhilfen", min_value=1, max_value=50, value=20)

with col2:
    minutes = st.number_input("Startzeit - Minuten", min_value=0, max_value=59, value=0)
    target_level = st.number_input("Ziel-Level", min_value=1, max_value=30, value=10)

initial_timer_seconds = hours * 3600 + minutes * 60
min_help = get_min_help_seconds(target_level, help_type)

if st.button("Berechnen"):
    remaining_time = initial_timer_seconds
    total_reduced = 0
    help_steps = []

    for i in range(1, helps + 1):
        percent_reduction = remaining_time * 0.01
        if percent_reduction >= min_help:
            reduction = percent_reduction
        else:
            reduction = min_help

        reduction = min(reduction, remaining_time)
        remaining_time -= reduction
        total_reduced += reduction

        help_steps.append((i, round(reduction), round(remaining_time)))

        if remaining_time <= 0:
            break

    st.subheader("Ergebnis")
    st.markdown(f"**Art:** {help_type}")
    st.markdown(f"**Gesamtzeit reduziert:** {round(total_reduced)} Sekunden ({seconds_to_h_m_s(round(total_reduced))})")
    st.markdown(f"**Verbleibende Zeit:** {round(remaining_time)} Sekunden ({seconds_to_h_m_s(round(remaining_time))})")

    st.markdown("---")
    st.subheader("Detaillierte Hilfe-Schritte")

    # Für Diagramm Daten vorbereiten
    df = pd.DataFrame({
        "Hilfe #": [row[0] for row in help_steps],
        "Zeit reduziert (Sek.)": [row[1] for row in help_steps],
        "Restzeit (Sek.)": [row[2] for row in help_steps],
    })

    # Linien-Diagramm für Restzeit
    fig = px.line(df, x="Hilfe #", y="Restzeit (Sek.)",
                  title=f"Restzeit nach jeder Allianzhilfe bei {help_type}",
                  labels={"Hilfe #": "Anzahl Allianzhilfen", "Restzeit (Sek.)": "Restzeit (Sekunden)"},
                  template="plotly_dark",
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.write(df)
