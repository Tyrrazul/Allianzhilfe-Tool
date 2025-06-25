import streamlit as st
import math

# Funktion: Mindesthilfezeit basierend auf Ziel-Level und Typ
def get_min_help_seconds(target_level, help_type):
    # Zeit in Sekunden je nach Levelbereich
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

# Streamlit UI
st.set_page_config(page_title="Allianzhilfe-Rechner", layout="centered")
st.title("🛠️ Warhammer: Chaos & Conquest - Allianzhilfe-Rechner")

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
