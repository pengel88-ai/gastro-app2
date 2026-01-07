import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. KONFIGURATION ---
st.set_page_config(page_title="GastroPro v1.9 - Demo Edition", page_icon="👨‍🍳", layout="wide")

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

# --- 3. DEMO-DATEN FUNKTION ---
def load_demo_data():
    # Beispiel Speisekarte
    st.session_state['rezepte'] = [
        {"Name": "Wiener Schnitzel (Kalb)", "Kat": "Speise", "VK": 24.50, "Marge %": 68.5},
        {"Name": "Lachsforelle Müllerin Art", "Kat": "Speise", "VK": 21.90, "Marge %": 72.1},
        {"Name": "Trüffel Pasta", "Kat": "Speise", "VK": 18.50, "Marge %": 75.0},
        {"Name": "Hausgemachte Limonade", "Kat": "Getränk", "VK": 5.50, "Marge %": 88.0},
        {"Name": "Gin Tonic (Hausmarke)", "Kat": "Getränk", "VK": 9.50, "Marge %": 82.5}
    ]
    # Beispiel Personal
    st.session_state['schichten'] = [
        {"Tag": "Montag", "Name": "Max (Küchenchef)", "Bereich": "Küche", "Kosten": 180.0, "Umsatz_Soll": 1200.0},
        {"Tag": "Montag", "Name": "Anna", "Bereich": "Service", "Kosten": 120.0, "Umsatz_Soll": 1200.0},
        {"Tag": "Dienstag", "Name": "Lukas", "Bereich": "Bar", "Kosten": 100.0, "Umsatz_Soll": 900.0},
        {"Tag": "Mittwoch", "Name": "Sven", "Bereich": "Spülküche", "Kosten": 80.0, "Umsatz_Soll": 1000.0},
        {"Tag": "Donnerstag", "Name": "Julia", "Bereich": "Overhead", "Kosten": 200.0, "Umsatz_Soll": 1500.0}
    ]
    st.success("Demo-Daten wurden geladen!")

if check_password():
    # Speicher initialisieren
    if 'rezepte' not in st.session_state: st.session
