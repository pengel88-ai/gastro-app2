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
    st.session_state['rezepte'] = [
        {"Name": "Wiener Schnitzel (Kalb)", "Kat": "Speise", "VK": 24.50, "Marge %": 68.5},
        {"Name": "Lachsforelle Müllerin Art", "Kat": "Speise", "VK": 21.90, "Marge %": 72.1},
        {"Name": "Trüffel Pasta", "Kat": "Speise", "VK": 18.50, "Marge %": 75.0},
        {"Name": "Hausgemachte Limonade", "Kat": "Getränk", "VK": 5.50, "Marge %": 88.0},
        {"Name": "Gin Tonic (Hausmarke)", "Kat": "Getränk", "VK": 9.50, "Marge %": 82.5}
    ]
    st.session_state['schichten'] = [
        {"Tag": "Montag", "Name": "Max (Küchenchef)", "Bereich": "Küche", "Kosten": 180.0, "Umsatz_Soll": 1200.0},
        {"Tag": "Montag", "Name": "Anna", "Bereich": "Service", "Kosten": 120.0, "Umsatz_Soll": 1200.0},
        {"Tag": "Dienstag", "Name": "Lukas", "Bereich": "Bar", "Kosten": 100.0, "Umsatz_Soll": 900.0}
    ]
    st.success("Demo-Daten wurden geladen!")

# --- 4. HAUPTPROGRAMM ---
if check_password():
    # DATENSPEICHER INITIALISIEREN (Hier war der Fehler!)
    if 'rezepte' not in st.session_state: 
        st.session_state['rezepte'] = []
    if 'schichten' not in st.session_state: 
        st.session_state['schichten'] = []

    tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    bereiche = ["Küche", "Service", "Spülküche", "Bar", "Overhead"]

    # --- SIDEBAR ---
    st.sidebar.title("👨‍🍳 GastroPro v1.9")
    if st.sidebar.button("✨ Demo-Daten laden"):
        load_demo_data()
        st.rerun()
    if st.sidebar.button("Logout"):
        st.session_state["password_correct"] = False
        st.rerun()
    
    page = st.sidebar.radio("Menü:", ["📊 Dashboard", "🍲 Kalkulation", "📅 Personal & Absatz", "📜 Speisekarte"])

    # --- DASHBOARD ---
    if page == "📊 Dashboard":
        st.header("📊 Kosten-Analyse")
        total_p = sum(s['Kosten'] for s in st.session_state['schichten'])
        c1, c2 = st.columns(2)
        c1.metric("Personal-Kosten (Woche)", f"{total_p:.2f} €")
        c2.metric("Rezepte in Datenbank", len(st.session_state['rezepte']))
        
        if st.session_state['schichten']:
            df_p = pd.DataFrame(st.session_state['schichten'])
            st.bar_chart(df_p.groupby("Bereich")["Kosten"].sum().reindex(bereiche).fillna(0))

    # --- KALKULATION ---
    elif page == "🍲 Kalkulation":
        st.header("🍲 Neue Kalkulation")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Bezeichnung")
            kat = st.selectbox("Kategorie", ["Speise", "Getränk"])
            ek = st.number_input("Warenwert Netto (€)", min_value=0.0, value=3.0)
        with col2:
            gemeinkosten = st.slider("Gemeinkosten Aufschlag %", 0, 100, 25)
            vk = st.number_input("Verkaufspreis Brutto (€)", min_value=0.0, value=15.0)
            mwst = st.radio("MwSt (%)", [19, 7], horizontal=True)

        netto_vk = vk / (1 + mwst/100)
        selbstkosten = ek * (1 + gemeinkosten/100)
        marge = ((netto_vk - selbstkosten) / netto_vk * 100) if netto_vk > 0 else 0

        if st.button("💾 Gericht speichern"):
            st.session_state['rezepte'].append({"Name": name, "Kat": kat, "VK": vk, "Marge %": round(marge, 1)})
            st.success(f"{name} gespeichert!")

    # --- PERSONAL & ABSATZ ---
    elif page == "📅 Personal & Absatz":
        st.header("📅 Wochenplanung")
        with st.expander("➕ Neue Schicht hinzufügen"):
            c1, c2 = st.columns(2)
            with c1:
                t = st.selectbox("Wochentag", tage); n = st.text_input("Name"); b = st.selectbox("Abteilung", bereiche)
            with c2:
                s = st.number_input("Stunden", value=8.0); l = st.number_input("Lohn", value=15.0); u = st.number_input("Tagesumsatz (€)", value=1000.0)
            if st.button("Schicht eintragen"):
                st.session_state['schichten'].append({"Tag": t, "Name": n, "Bereich": b, "Kosten": s*l*1.2, "Umsatz_Soll": u})
                st.rerun()

        for tag in tage:
            tag_schichten = [s for s in st.session_state['schichten'] if s['Tag'] == tag]
            if tag_schichten:
                with st.expander(f"📌 {tag}", expanded=True):
                    t_kosten = sum(s['Kosten'] for s in tag_schichten)
                    t_umsatz = tag_schichten[0]['Umsatz_Soll']
                    st.write(f"Personal: {t_kosten:.2f} € | Ziel: {t_umsatz:.2f} €")
                    for i, schicht in enumerate(st.session_state['schichten']):
                        if schicht['Tag'] == tag:
                            c_n, c_d = st.columns([5,1])
                            c_n.write(f"• {schicht['Name']} ({schicht['Bereich']})")
                            if c_d.button("🗑️", key=f"del_p_{tag}_{i}"):
                                st.session_state['schichten'].pop(i)
                                st.rerun()

    # --- SPEISEKARTE ---
    elif page == "📜 Speisekarte":
        st.header("📜 Karte")
        if st.session_state['rezepte']:
            for i, r in enumerate(st.session_state['rezepte']):
                c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                c1.write(f"**{r['Name']}**")
                c2.write(f"{r['VK']:.2f} €")
                c3.write(f"{r['Marge %']}%")
                if c4.button("🗑️", key=f"del_rez_{i}"):
                    st.session_state['rezepte'].pop(i)
                    st.rerun()
