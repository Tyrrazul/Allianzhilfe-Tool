import streamlit as st
import math
import altair as alt
import pandas as pd

# Hintergrund & Göttersymbole anzeigen
def set_custom_background_and_icons():
    background_url = "https://raw.githubusercontent.com/Tyrrazul/Allianzhilfe-Tool/main/Papyrus%20background.png"
    khorne_url = "https://raw.githubusercontent.com/Tyrrazul/Allianzhilfe-Tool/main/khorne.png"
    nurgle_url = "https://raw.githubusercontent.com/Tyrrazul/Allianzhilfe-Tool/main/nurgle.png"
    slaanesh_url = "https://raw.githubusercontent.com/Tyrrazul/Allianzhilfe-Tool/main/slaanesh.png"
    tzeentch_url = "https://raw.githubusercontent.com/Tyrrazul/Allianzhilfe-Tool/main/tzeentch.png"

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('{background_url}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #dddcdc;
        font-family: 'Garamond', serif;
    }}

    .corner-icon {{
        position: fixed;
        width: 240px;
        height: 240px;
        z-index: 999;
        opacity: 0.85;
    }}

    #slaanesh {{ top: 10px; left: 10px; }}
    #nurgle {{ top: 10px; right: 10px; }}
    #khorne {{ bottom: 10px; left: 10px; }}
    #tzeentch {{ bottom: 10px; right: 10px; }}

    /* Grimdark Style Buttons */
    .stButton>button {{
        background-color: #550000;
        color: #fff;
        border: 2px solid #a00;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5em 1em;
        box-shadow: 2px 2px 8px #000;
        transition: 0.2s ease-in-out;
        font-family: 'Garamond', serif;
    }}

    .stButton>button:hover {{
        background-color: #770000;
        transform: scale(1.05);
        box-shadow: 3px 3px 12px #000;
    }}

    /* Dataframe Styling */
    .stDataFrameContainer {{
        background-color: rgba(10, 10, 10, 0.7);
        border: 1px solid #440000;
        border-radius: 6px;
        padding: 1em;
        box-shadow: 2px 2px 6px #000;
        color: #dddcdc !important;
    }}
    </style>

    <img src="{slaanesh_url}" class="corner-icon" id="slaanesh" />
    <img src="{nurgle_url}" class="corner-icon" id="nurgle" />
    <img src="{khorne_url}" class="corner-icon" id="khorne" />
    <img src="{tzeentch_url}" class="corner-icon" id="tzeentch" />
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
            (1, 6): 60,
            (7, 7): 180,
            (8, 8): 300,
            (9, 11): 600,
            (12, 14): 1200,
            (15, 15): 2400,
            (16, 18): 3600,
            (19, 20): 5400,
            (21, 30): 7200
        }
    }
    table = help_table.get(help_type, help_table["Gebäude"])
    for level_range, seconds in table.items():
        if level_range[0] <= target_level <= level_range[1]:
            return seconds
    return 60

# Seite konfigurieren
st.set_page_config(page_title="Allianzhilfe-Rechner", layout="centered")

st.title("🛠️ Warhammer: Chaos & Conquest - Allianzhilfe-Rechner")
st.markdown("""
Berechne, wie viel Zeit du bei **Gebäuden** oder **Ritualen** durch Allianzhilfe einsparst.
""")

# Auswahl Gebäude oder Ritual
help_type = st.selectbox("Was möchtest du berechnen?", ["Gebäude", "Ritual"])

# Eingabefelder
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

    # Umrechnung verbleibende Zeit in Stunden, Minuten, Sekunden
    hours_r = remaining_time // 3600
    remainder = remaining_time % 3600
    minutes_r = remainder // 60
    seconds_r = remainder % 60

    st.subheader("🧞 Ergebnis")
    st.markdown(f"**Art:** {help_type}")
    st.markdown(f"**Gesamtzeit reduziert:** {round(total_reduced)} Sekunden")
    st.markdown(f"**Verbleibende Zeit:** {round(remaining_time)} Sekunden")
    st.markdown(f"➡️ **{minutes_r} Minuten {seconds_r} Sekunden** / **{hours_r} Stunden {minutes_r} Minuten**")

    st.markdown("---")
    st.subheader("📊 Detaillierte Hilfe-Schritte")

    # DataFrame aus den Schritten
    df = pd.DataFrame(help_steps, columns=["Hilfe #", "Zeit reduziert (s)", "Restzeit (s)"])

    # Altair Chart erstellen
    base = alt.Chart(df).encode(
        x=alt.X("Hilfe #", title="Allianzhilfe Nr."),
        tooltip=[
            alt.Tooltip("Hilfe #", title="Hilfe Nr."),
            alt.Tooltip("Zeit reduziert (s)", title="Zeit reduziert (Sek.)"),
            alt.Tooltip("Restzeit (s)", title="Verbleibende Zeit (Sek.)")
        ]
    )

    # Balken für reduzierte Zeit
    bars = base.mark_bar(color="#990000", cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        y=alt.Y("Zeit reduziert (s)", title="Sekunden reduziert"),
    )

    # Linie für Restzeit
    line = base.mark_line(color="#cc5555", strokeWidth=3, point=True).encode(
        y=alt.Y("Restzeit (s)", title="Verbleibende Zeit (Sek.)")
    )

    chart = alt.layer(bars, line).resolve_scale(
        y='independent'
    ).properties(
        width=700,
        height=400,
        background="#1e1e1e"
    ).configure_axis(
        labelColor="#dddcdc",
        titleColor="#ff9999",
        gridColor="#330000"
    ).configure_view(
        strokeWidth=0
    ).configure_title(
        fontSize=18,
        color="#ff9999",
        font='Garamond'
    )

    st.altair_chart(chart, use_container_width=True)
