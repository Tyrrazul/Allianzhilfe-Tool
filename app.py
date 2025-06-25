import streamlit as st
import math
import altair as alt
import pandas as pd

# Seite konfigurieren
st.set_page_config(page_title="Allianzhilfe-Rechner", layout="centered")

# CSS Styling mit Google Font und Grimdark Style
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=UnifrakturCook:wght@700&display=swap');

    /* Gesamte App Schrift + Farben */
    .stApp {
        font-family: 'UnifrakturCook', cursive;
        background-color: #1a1a1a;
        color: #e6e2dc;
        background-image: url('https://i.imgur.com/3vzHKDM.png'); /* leichte Blutspritzer */
        background-repeat: no-repeat;
        background-position: center top;
        background-size: 150px 150px;
    }

    /* Überschriften */
    h1, h2, h3, h4 {
        color: #b30000;
        text-shadow: 1.5px 1.5px 3px #000;
        font-weight: 700;
    }

    /* Buttons Styling */
    .stButton>button {
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
    }
    .stButton>button:hover {
        background-color: #770000;
        transform: scale(1.05);
        box-shadow: 3px 3px 12px #330000;
    }
    </style>
""", unsafe_allow_html=True)

# Titel ohne Emojis
st.title("Warhammer: Chaos & Conquest - Allianzhilfe-Rechner")

st.markdown("""
Berechne, wie viel Zeit du bei **Gebäuden** oder **Ritualen** durch Allianzhilfe einsparst.
""")

# Mindesthilfezeit Funktion
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

# User Inputs
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

    # Umrechnung verbleibende Zeit in Stunden, Minuten, Sekunden
    hours_r = remaining_time // 3600
    remainder = remaining_time % 3600
    minutes_r = remainder // 60
    seconds_r = remainder % 60

    st.subheader("Ergebnis")
    st.markdown(f"**Art:** {help_type}")
    st.markdown(f"**Gesamtzeit reduziert:** {round(total_reduced)} Sekunden")
    st.markdown(f"**Verbleibende Zeit:** {round(remaining_time)} Sekunden")
    st.markdown(f"➡️ {hours_r} Stunden {minutes_r} Minuten {seconds_r} Sekunden")

    st.markdown("---")
    st.subheader("Detaillierte Hilfe-Schritte")

    # Dataframe für Altair
    df = pd.DataFrame(help_steps, columns=["Hilfe #", "Zeit reduziert (s)", "Restzeit (s)"])

    # Korrekte Werte aus der Berechnung - fürs Diagramm
    # Zeit reduziert als Balken, Restzeit als Linie (zweite Y-Achse)

    base = alt.Chart(df).encode(
        x=alt.X("Hilfe #", title="Allianzhilfe Nr."),
        tooltip=[
            alt.Tooltip("Hilfe #", title="Hilfe Nr."),
            alt.Tooltip("Zeit reduziert (s)", title="Zeit reduziert (Sek.)"),
            alt.Tooltip("Restzeit (s)", title="Verbleibende Zeit (Sek.)"),
        ]
    )

    bars = base.mark_bar(color="#8B0000", cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        y=alt.Y("Zeit reduziert (s)", title="Sekunden reduziert"),
    )

    line = base.mark_line(color="#FF4500", strokeWidth=3, point=True).encode(
        y=alt.Y("Restzeit (s)", title="Verbleibende Zeit (Sek.)"),
    )

    layered_chart = alt.layer(bars, line).resolve_scale(
        y='independent'
    ).properties(
        width=700,
        height=400,
        background="#2a2a2a",
        title=f"Hilfe-Schritte: Zeit reduziert und Restzeit ({help_type})"
    ).configure_title(
        fontSize=20,
        font='UnifrakturCook',
        color='#b30000'
    ).configure_axis(
        labelColor="#e6e2dc",
        titleColor="#b30000",
        gridColor="#660000"
    ).configure_view(
        strokeWidth=0
    )

    st.altair_chart(layered_chart, use_container_width=True)
