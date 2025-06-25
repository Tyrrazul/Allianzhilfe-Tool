import streamlit as st
import math

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

    /* Button-Styling */
    .stButton>button {{
        background-color: #550000;
        color: #fff;
        border: 2px solid #a00;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5em 1em;
        box-shadow: 2px 2px 8px #000;
        transition: 0.2s ease-in-out;
    }}

    .stButton>button:hover {{
        background-color: #770000;
        transform: scale(1.05);
        box-shadow: 3px 3px 12px #000;
    }}

    /* Eingabefeld-Hintergründe */
    .stNumberInput input {{
        background-color: rgba(0,0,0,0.5);
        color: white;
        border: 1px solid #a00;
    }}

    .stSelectbox div[data-baseweb="select"] > div {{
        background-color: rgba(0,0,0,0.5);
        color: white;
        border: 1px solid #a00;
    }}
    </style>

    <img src="{slaanesh_url}" class="corner-icon" id="slaanesh">
    <img src="{nurgle_url}" class="corner-icon" id="nurgle">
    <img src="{khorne_url}" class="corner-icon" id="khorne">
    <img src="{tzeentch_url}" class="corner-icon" id="tzeentch">
    """, unsafe_allow_html=True)

set_custom_background_and_icons()

# Funktion: Mindesthilfezeit basierend auf Ziel-Level und Typ
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
            (1, 1): 60,
            (2, 2): 180,
            (3, 3): 300,
            (4, 4): 600,
            (5, 5): 1200,
            (6, 6): 2400,
            (7, 7): 3600,
            (8, 8): 5400,
            (9, 9): 7200,
            (10, 10): 14400
        }
    }
    table = help_table.get(help_type, help_table["Gebäude"])
    for level_range, seconds in table.items():
        if level_range[0] <= target_level <= level_range[1]:
            return seconds
    return 60

# Streamlit UI
st.set_page_config(page_title="Allianzhilfe-Rechner", layout="centered")
st.title("Warhammer: Chaos & Conquest - Allianzhilfe-Rechner")

st.markdown("""
Berechne, wie viel Zeit du bei **Gebäuden** oder **Ritualen** durch Allianzhilfe einsparst.
""")

# Auswahl: Gebäude oder Ritual
help_type = st.selectbox("Was möchtest du berechnen?", ["Gebäude", "Ritual"])

# Eingaben
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

    # Zeitformatierung korrekt berechnen
    rem_h = int(remaining_time) // 3600
    rem_m = (int(remaining_time) % 3600) // 60
    rem_s = int(remaining_time) % 60

    total_minutes = int(remaining_time) // 60
    only_seconds = int(remaining_time) % 60

    st.subheader("Ergebnis")
    st.markdown(f"**Art:** {help_type}")
    st.markdown(f"**Gesamtzeit reduziert:** {round(total_reduced)} Sekunden")
    st.markdown(f"**Verbleibende Zeit:** {int(remaining_time)} Sekunden")
    st.markdown(f"**{total_minutes} Minuten {only_seconds} Sekunden**")
    st.markdown(f"**{rem_h} Stunden {rem_m} Minuten**")

    st.markdown("---")
    st.subheader("Detaillierte Hilfe-Schritte")
    st.write("Jede Zeile zeigt die Wirkung einer einzelnen Allianzhilfe.")
    st.dataframe({
        "Hilfe #": [row[0] for row in help_steps],
        "Zeit reduziert (s)": [row[1] for row in help_steps],
        "Restzeit (s)": [row[2] for row in help_steps],
    })
