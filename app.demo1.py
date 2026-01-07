import streamlit as st
import pandas as pd

# --- 1. SETTINGS ---
st.set_page_config(page_title="GastroPro v2.0", layout="wide")

# --- 2. LOGIN ---
def check_password():
    if "auth" not in st.session_state: st.session_state["auth"] = False
    if not st.session_state["auth"]:
        st.title("🔐 Login")
        pwd = st.text_input("Passwort", type="password")
        if st.button("Go"):
            if pwd == "Gastro2026":
                st.session_state["auth"] = True
                st.rerun()
        return False
    return True

# --- 3. DEMO DATEN ---
def load_demo():
    # Kompakte Liste um Zeilenumbrüche zu vermeiden
    st.session_state['rezepte'] = [
        {"Name": "Carpaccio", "Kat": "Vorspeise", "VK": 14.5, "M": 70},
        {"Name": "Schafskäse", "Kat": "Vorspeise", "VK": 9.8, "M": 75},
        {"Name": "Suppe", "Kat": "Vorspeise", "VK": 7.5, "M": 82},
        {"Name": "Rostbraten", "Kat": "Hauptgang", "VK": 28.5, "M": 64},
        {"Name": "Lachs", "Kat": "Hauptgang", "VK": 24.9, "M": 68},
        {"Name": "Bowl", "Kat": "Hauptgang", "VK": 16.5, "M": 78},
        {"Name": "Gulasch", "Kat": "Hauptgang", "VK": 22.5, "M": 66},
        {"Name": "Strudel", "Kat": "Dessert", "VK": 7.9, "M": 74},
        {"Name": "Brulee", "Kat": "Dessert", "VK": 8.5, "M": 77},
        {"Name": "Eis", "Kat": "Dessert", "VK": 9.2, "M": 81},
        {"Name": "Wein Weiß", "Kat": "Wein", "VK": 7.5, "M": 80},
        {"Name": "Wein Rot", "Kat": "Wein", "VK": 8.2, "M": 79},
        {"Name": "Bier", "Kat": "Bier", "VK": 5.2, "M": 84},
        {"Name": "Radler", "Kat": "Bier", "VK": 4.8, "M": 86},
        {"Name": "Cola", "Kat": "AFG", "VK": 4.5, "M": 88},
        {"Name": "Wasser", "Kat": "AFG", "VK": 6.9, "M": 92},
        {"Name": "Mojito", "Kat": "Cocktails", "VK": 10.5, "M": 83},
        {"Name": "Mule", "Kat": "Cocktails", "VK": 11.0, "M": 81},
        {"Name": "Kaffee", "Kat": "Heißgetränke", "VK": 4.2, "M": 89},
        {"Name": "Tee", "Kat": "Heißgetränke", "VK": 3.8, "M": 93}
    ]
    st.session_state['schichten'] = [
        {"Tag":"Mo", "Name":"Thomas", "Bereich":"Küche", "Kosten":190, "Ziel":2000},
        {"Tag":"Mo", "Name":"Stefan", "Bereich":"Küche", "Kosten":160
