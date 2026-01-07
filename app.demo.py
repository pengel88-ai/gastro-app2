import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai

# --- 1. KONFIGURATION & AI SETUP ---
st.set_page_config(page_title="GastroPro v1.9 - Demo Edition", page_icon="👨‍🍳", layout="wide")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    ai_available = True
else:
    ai_available = False

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
    # Beispiel Personal für Montag & Dienstag
    st.session_state['schichten'] = [
        {"Tag": "Montag", "Name": "Max (Chef)", "Bereich": "Küche", "Kosten": 180.0, "Umsatz_Soll": 1200.0},
        {"Tag": "Montag", "Name": "Anna", "Bereich": "Service", "Kosten": 120.0, "Umsatz_Soll": 1200.0},
        {"Tag": "Montag", "Name": "Lukas", "Bereich": "Bar", "Kosten": 100.0, "Umsatz_Soll": 1200.0},
        {"Tag": "Dienstag", "Name": "Sven", "Bereich": "Küche", "Kosten": 150.0, "Umsatz_Soll": 900.0},
        {"Tag": "Dienstag", "Name": "Maria", "Bereich": "Service", "Kosten": 110.0, "Umsatz_Soll": 900.0}
    ]
    st.success("Demo-Daten erfolgreich geladen!")

if check_password():
    if 'rezepte' not in st.session_state: st.session_state['rezepte'] = []
    if 'schichten' not in st.session_state: st.session_state['schichten'] = []

    tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    bereiche = ["Küche", "Service", "Spülküche", "Bar", "Overhead"]

    # --- SIDEBAR ---
    st.sidebar.title("👨‍🍳 GastroPro v1.9")
    
    # NEU: Demo Button
    if st.sidebar.button("✨ Demo-Daten laden"):
        load_demo_data()
        st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state["password_correct"] = False
        st.rerun()
    
    page = st.sidebar.radio("Menü:", ["📊 Dashboard", "🤖 AI-Rezept-Assistent", "🍲 Kalkulation", "📅 Personal & Absatz", "📜 Speisekarte"])

    # --- 1. DASHBOARD ---
    if page == "📊 Dashboard":
        st.header("📊 Kosten-Analyse")
        total_p = sum(s['Kosten'] for s in st.session_state['schichten'])
        c1, c2 = st.columns(2)
        c1.metric("Personal-Kosten/Woche", f"{total_p:.2f} €")
        c2.metric("Rezepte in Datenbank", len(st.session_state['rezepte']))
        
        if st.session_state['schichten']:
            df_p = pd.DataFrame(st.session_state['schichten'])
            st.subheader("Kosten nach Bereich")
            st.bar_chart(df_p.groupby("Bereich")["Kosten"].sum().reindex(bereiche).fillna(0))

    # --- 2. AI REZEPT ---
    elif page == "🤖 AI-Rezept-Assistent":
        st.header("🤖 KI-Gastro-Berater")
        if not ai_available:
            st.warning("⚠️ Bitte hinterlege den GEMINI_API_KEY in den Streamlit Secrets.")
        else:
            user_input = st.text_input("Zutat oder Gericht-Idee:", placeholder="z.B. Veganer Burger")
            if st.button("KI-Vorschlag generieren"):
                with st.spinner("Berechne..."):
                    try:
                        model = genai.GenerativeModel('gemini-pro')
                        prompt = f"Erstelle ein Gastro-Rezept für: {user_input}. Format: Name; Kategorie; EK; VK; Kurzbeschreibung"
                        response = model.generate_content(prompt)
                        data = response.text.split(";")
                        if len(data) >= 4:
                            st.info(f"Vorschlag: {data[0]} | Empfohlener VK: {data[3]} €")
                            if st.button("Übernehmen"):
                                st.session_state['rezepte'].append({"Name": data[0], "Kat": data[1], "VK": float(data[3].replace("€","")), "Marge %": 70.0})
                                st.rerun()
                    except: st.error("Fehler.")

    # --- 3. KALKULATION ---
    elif page == "🍲 Kalkulation":
        st.header("🍲 Neue Kalkulation")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Bezeichnung")
            kat = st.selectbox("Kat", ["Speise", "Getränk"])
            ek = st.number_input("EK Netto (€)", value=3.0)
        with col2:
            vk = st.number_input("VK Brutto (€)", value=15.0)
            if st.button("Speichern"):
                st.session_state['rezepte'].append({"Name": name, "Kat": kat, "VK": vk, "Marge %": 72.0})
                st.success("Gespeichert!")

    # --- 4. PERSONAL & ABSATZ-CHECK ---
    elif page == "📅 Personal & Absatz":
        st.header("📅 Wochenplanung")
        with st.expander("➕ Schicht hinzufügen"):
            c1, c2 = st.columns(2)
            with c1:
                t = st.selectbox("Tag", tage); n = st.text_input("Name"); b = st.selectbox("Bereich", bereiche)
            with c2:
                s = st.number_input("Stunden", value=8.0); l = st.number_input("Lohn", value=15.0); u = st.number_input("Ziel-Umsatz", value=1000.0)
            if st.button("Hinzufügen"):
                st.session_state['schichten'].append({"Tag": t, "Name": n, "Bereich": b, "Kosten": s*l*1.2, "Umsatz_Soll": u})
                st.rerun()

        for tag in tage:
            schichten = [s for s in st.session_state['schichten'] if s['Tag'] == tag]
            if schichten:
                with st.expander(f"📌 {tag}", expanded=True):
                    t_umsatz = schichten[0]['Umsatz_Soll']
                    st.write(f"Ziel-Umsatz: **{t_umsatz:.2f} €**")
                    # Absatz-Check
                    if st.session_state['rezepte']:
                        df_r = pd.DataFrame(st.session_state['rezepte'])
                        avg_v = df_r['VK'].mean()
                        anzahl = t_umsatz / avg_v if avg_v > 0 else 0
                        st.metric("Benötigte Verkäufe (Ø)", f"ca. {int(anzahl)} Einheiten", f"Ø-Preis {avg_v:.2f}€")
                    
                    for i, s in enumerate(st.session_state['schichten']):
                        if s['Tag'] == tag:
                            col_n, col_d = st.columns([4,1])
                            col_n.write(f"{s['Name']} ({s['Bereich']}) - {s['Kosten']:.2f} €")
                            if col_d.button("🗑️", key=f"del_{tag}_{i}"):
                                st.session_state['schichten'].pop(i)
                                st.rerun()

    # --- 5. SPEISEKARTE ---
    elif page == "📜 Speisekarte":
        st.header("📜 Aktuelle Karte")
        if st.session_state['rezepte']:
            for i, r in enumerate(st.session_state['rezepte']):
                c1, c2, c3 = st.columns([4,2,1])
                c1.write(f"**{r['Name']}** ({r['Kat']})")
                c2.write(f"{r['VK']:.2f} €")
                if c3.button("🗑️", key=f"del_rez_{i}"):
                    st.session_state['rezepte'].pop(i)
                    st.rerun()
            if st.button("⚠️ Alle löschen"):
                st.session_state['rezepte'] = []
                st.rerun()
