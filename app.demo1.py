import streamlit as st
import pandas as pd

# --- 1. KONFIGURATION ---
st.set_page_config(page_title="GastroPro v1.9.8 - Full Show", page_icon="👨‍🍳", layout="wide")

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
    # Speisekarte Erweiterung
    st.session_state['rezepte'] = [
        # VORSPEISEN
        {"Name": "Rinder Carpaccio", "Kat": "Vorspeise", "VK": 14.50, "Marge %": 70.0, "Rezept": "80g Rinderfilet, Rucola, Parmesan, Olivenöl, Zitrone"},
        {"Name": "Gebackener Schafskäse", "Kat": "Vorspeise", "VK": 9.80, "Marge %": 75.2, "Rezept": "150g Feta, Oliven, Zwiebeln, Fladenbrot"},
        {"Name": "Tomaten-Basilikum Suppe", "Kat": "Vorspeise", "VK": 7.50, "Marge %": 82.0, "Rezept": "Frische Tomaten, Sahne-Haube, Baguette"},
        
        # HAUPTGÄNGE
        {"Name": "Zwiebelrostbraten", "Kat": "Hauptgang", "VK": 28.50, "Marge %": 64.0, "Rezept": "220g Roastbeef, Röstzwiebeln, Spätzle, Jus"},
        {"Name": "Lachs-Filet vom Grill", "Kat": "Hauptgang", "VK": 24.90, "Marge %": 68.5, "Rezept": "200g Lachs, Grillgemüse, Rosmarinkartoffeln"},
        {"Name": "Vegane Bowl", "Kat": "Hauptgang", "VK": 16.50, "Marge %": 78.0, "Rezept": "Quinoa, Avocado, Kichererbsen, Tahini-Dressing"},
        {"Name": "Wildschwein-Gulasch", "Kat": "Hauptgang", "VK": 22.50, "Marge %": 66.0, "Rezept": "Wildfleisch, Preiselbeeren, Semmelknödel"},
        
        # DESSERTS
        {"Name": "Apfelstrudel", "Kat": "Dessert", "VK": 7.90, "Marge %": 74.0, "Rezept": "Hausgemacht, Vanillesauce, Sahne"},
        {"Name": "Crème Brûlée", "Kat": "Dessert", "VK": 8.50, "Marge %": 77.0, "Rezept": "Eigelb, Sahne, echte Vanille, Rohrzucker"},
        {"Name": "Eisbecher 'GastroPro'", "Kat": "Dessert", "VK": 9.20, "Marge %": 81.0, "Rezept": "3 Kugeln, Früchte der Saison, Sahne"},

        # GETRÄNKE (10 neue Produkte)
        {"Name": "Grauburgunder 0,2l", "Kat": "Wein", "VK": 7.50, "Marge %": 80.0, "Rezept": "Winzerhof XY"},
        {"Name": "Primitivo 0,2l", "Kat": "Wein", "VK": 8.20, "Marge %": 79.0, "Rezept": "Italien, vollmundig"},
        {"Name": "Weizenbier 0,5l", "Kat": "Bier", "VK": 5.20, "Marge %": 84.0, "Rezept": "Flasche"},
        {"Name": "Radler 0,5l", "Kat": "Bier", "VK": 4.80, "Marge %": 86.0, "Rezept": "Hausmarke"},
        {"Name": "Cola / Fanta 0,4l", "Kat": "AFG", "VK": 4.50, "Marge %": 88.0, "Rezept": "Glasware"},
        {"Name": "Mineralwasser 0,75l", "Kat": "AFG", "VK": 6.90, "Marge %": 92.0, "Rezept": "Premium
