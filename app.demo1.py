import streamlit as st
import pandas as pd

# --- 1. KONFIGURATION ---
st.set_page_config(page_title="GastroPro v1.9.9", page_icon="👨‍🍳", layout="wide")

# --- 2. PASSWORT-SCHUTZ ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if not st.session_state["password_correct"]:
        st.title("🔐 GastroPro Login")
        pwd = st.text_input("Passwort", type="password")
        if st.button("Anmelden"):
            if pwd == "Gastro2026": 
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Passwort falsch.")
        return False
    return True

# --- 3. MASSIV ERWEITERTE DEMO-DATEN ---
def load_demo_data():
    # Speisekarte
    st.session_state['rezepte'] = [
        {"Name": "Rinder Carpaccio", "Kat": "Vorspeise", "VK": 14.50, "Marge %": 70.0, "Rezept": "Rinderfilet, Rucola, Parmesan"},
        {"Name": "Gebackener Schafskäse", "Kat": "Vorspeise", "VK": 9.80, "Marge %": 75.2, "Rezept": "Feta, Oliven, Zwiebeln"},
        {"Name": "Tomatensuppe", "Kat": "Vorspeise", "VK": 7.50, "Marge %": 82.0, "Rezept": "Tomaten, Sahne, Baguette"},
        {"Name": "Zwiebelrostbraten", "Kat": "Hauptgang", "VK": 28.50, "Marge %": 64.0, "Rezept": "Roastbeef, Spätzle, Jus"},
        {"Name": "Lachs-Filet", "Kat": "Hauptgang", "VK": 24.90, "Marge %": 68.5, "Rezept": "Lachs, Grillgemüse"},
        {"Name": "Vegane Bowl", "Kat": "Hauptgang", "VK": 16.50, "Marge %": 78.0, "Rezept": "Quinoa, Avocado, Tahini"},
        {"Name": "Wildschwein-Gulasch", "Kat": "Hauptgang", "VK": 22.50, "Marge %": 66.0, "Rezept": "Wild, Preiselbeeren, Knödel"},
        {"Name": "Apfelstrudel", "Kat": "Dessert", "VK": 7.90, "M
