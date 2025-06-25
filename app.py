import streamlit as st
import math

# URLs der Raw-Bilder aus deinem Repo
papyrus_url = "https://raw.githubusercontent.com/Tyrrazul/Allianzhilfe-Tool/main/Papyrus%20background.png"
nurgle_url = "https://raw.githubusercontent.com/Tyrrazul/Allianzhilfe-Tool/main/Nurgle.webp"
khorne_url = "https://raw.githubusercontent.com/Tyrrazul/Allianzhilfe-Tool/main/Mark_of_Khorne.webp"
slaanesh_url = "https://raw.githubusercontent.com/Tyrrazul/Allianzhilfe-Tool/main/Slaanesh%20Symbol.webp"
tzeentch_url = "https://raw.githubusercontent.com/Tyrrazul/Allianzhilfe-Tool/main/Tzeentch.webp"

# CSS: Hintergrund + Gottessymbole mit Zahlen
st.markdown(f"""
<style>
/* Hintergrundbild (Papyrus), fixed und komplett */
[data-testid="stAppViewContainer"] {{
    background-image: url("{papyrus_url}");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    background-repeat: no-repeat;
}}

/* Container für Göttersymbole */
.gott-symbol {{
    position: fixed;
    width: 80px;
    height: 80px;
    opacity: 0.85;
    z-index: 100;
}}

/* Zahl über den Symbolen */
.gott-zahl {{
    position: fixed;
    font-size: 24px;
    font-weight: bold;
    color: #4a2600;
    text-shadow: 2px 2px 4px #fff8dc;
    font-family: 'Georgia', serif;
    z-index: 110;
}}

/* Slaanesh (oben links, Zahl 6) */
#slaanesh-img {{
    top: 20px;
    left: 20px;
}}

#slaanesh-num {{
    top: 5px;
    left: 55px;
}}

/* Nurgle (oben rechts, Zahl 7) */
#nurgle-img {{
    top: 20px;
    right: 20px;
}}

#nurgle-num {{
    top: 5px;
    right: 55px;
}}

/* Khorne (unten links, Zahl 8) */
#khorne-img {{
    bottom: 20px;
    left: 20px;
}}

#khorne-num {{
    bottom: 105px;
    left: 55px;
}}

/* Tzeentch (unten rechts, Zahl 9) */
#tzeentch-img {{
    bottom: 20px;
    right: 20px;
}}

#tzeentch-num {{
    bottom: 105px;
    right: 55px;
}}

/* Hauptcontainer etwas transparent, damit Hintergrund sichtbar bleibt */
[data-testid="stVerticalBlock"] > div:first-child {{
    background-color: rgba(255, 255, 240, 0.8);
    border-radius: 10px;
    padding: 20px;
    max-width: 700px;
    margin: 40px auto 80px auto;
}}

/* Überschrift */
h1 {{
    font-family: 'Georgia', serif;
    color: #4a2600;
    text-shadow: 1px 1px 2px #d2b48c;
}}

</style>

<!-- Göttersymbole + Zahlen -->
<div>
    <img id="slaanesh-img" class="gott-symbol" src="{slaanesh_url}" alt="Slaanesh" />
    <div id="slaanesh-num" class="gott-zahl">6</div>

    <img id="nurgle-img" class="gott-symbol" src="{nurgle_url}" alt="Nurgle" />
    <div id="nurgle-num" class="gott-zahl">7</div>

    <img id="khorne-img" class="gott-symbol" src="{khorne_url}" alt="Khorne" />
    <div id="khorne-num" class="gott-zahl">8</div>

    <img id="tzeentch-img" class="gott-symbol" src="{tzeentch_url}" alt="Tzeentch" />
    <div id="tzeentch-num" class="gott-zahl">9</div>
</div>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Allianzhilfe-Rechner", layout="centered")
st.title("🛠️ Warhammer: Chaos & Conquest - Allianzhilfe-Rechner")

st.markdown("""
Berechne, wie viel Zeit du bei **Gebäuden** oder **Ritualen** durch Allianzhilfe einsparst.
""")

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

    # Ausgabe
    st.subheader("🧾 Ergebnis")
    st.markdown(f"**Art:** {help_type}")
    st.markdown(f"**Gesamtzeit reduziert:** {round(total_reduced)} Sekunden")
    st.markdown(f"**Verbleibende Zeit:** {round(remaining_time)} Sekunden")
    st.markdown(f"➡️ **{round(remaining_time / 60, 2)} Minuten** / **{round(remaining_time / 3600, 2)} Stunden**")

    st.markdown("---")
    st.subheader("📊 Detaillierte Hilfe-Schritte")
    st.write("Jede Zeile zeigt die Wirkung einer einzelnen Allianzhilfe.")
    st.dataframe({
        "Hilfe #": [row[0] for row in help_steps],
        "Zeit reduziert (s)": [row[1] for row in help_steps],
        "Restzeit (s)": [row[2] for row in help_steps],
    })


