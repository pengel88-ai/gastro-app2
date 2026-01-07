import streamlit as st
import pandas as pd

# --- 1. SETTINGS ---
st.set_page_config(page_title="GastroPro v2.1", layout="wide")

# --- 2. LOGIN ---
def check_password():
    if "auth" not in st.session_state: st.session_state["auth"] = False
    if not st.session_state["auth"]:
        st.title("🔐 GastroPro Login")
        pwd = st.text_input("Passwort", type="password")
        if st.button("Anmelden"):
            if pwd == "Gastro2026":
                st.session_state["auth"] = True
                st.rerun()
        return False
    return True

# --- 3. DEMO DATEN FUNKTION ---
def load_demo():
    # Speisen
    s1 = {"Name": "Rinder Carpaccio", "Kat": "Vorspeise", "VK": 14.5, "M": 70}
    s2 = {"Name": "Gebackener Feta", "Kat": "Vorspeise", "VK": 9.8, "M": 75}
    s3 = {"Name": "Tomatensuppe", "Kat": "Vorspeise", "VK": 7.5, "M": 82}
    s4 = {"Name": "Zwiebelrostbraten", "Kat": "Hauptgang", "VK": 28.5, "M": 64}
    s5 = {"Name": "Lachs-Filet", "Kat": "Hauptgang", "VK": 24.9, "M": 68}
    s6 = {"Name": "Vegane Bowl", "Kat": "Hauptgang", "VK": 16.5, "M": 78}
    s7 = {"Name": "Apfelstrudel", "Kat": "Dessert", "VK": 7.9, "M": 74}
    s8 = {"Name": "Crème Brûlée", "Kat": "Dessert", "VK": 8.5, "M": 77}
    
    # Getränke
    g1 = {"Name": "Grauburgunder", "Kat": "Wein", "VK": 7.5, "M": 80}
    g2 = {"Name": "Pils 0,5l", "Kat": "Bier", "VK": 4.9, "M": 85}
    g3 = {"Name": "Cola 0,4l", "Kat": "AFG", "VK": 4.5, "M": 88}
    g4 = {"Name": "Moscow Mule", "Kat": "Cocktails", "VK": 11.0, "M": 81}
    g5 = {"Name": "Cappuccino", "Kat": "Heißgetränke", "VK": 4.2, "M": 89}
    
    st.session_state['rezepte'] = [s1, s2, s3, s4, s5, s6, s7, s8, g1, g2, g3, g4, g5
