import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. GRUNDEINSTELLUNGEN ---
st.set_page_config(page_title="GastroPro v1.7", page_icon="👨‍🍳", layout="wide")

# --- 2. PASSWORT-FUNKTION ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if not st.session_state["password_correct"]:
        st.title("🔐 GastroPro Login")
        pwd = st.text_input("Bitte Passwort eingeben", type="password")
        if st.button("Anmelden"):
            if pwd == "Gastro2026": 
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Passwort falsch.")
        return False
    return True

if check_password():
    # Daten-Speicher initialisieren
    if 'rezepte' not in st.session_state: st.session_state['rezepte'] = []
    if 'schichten' not in st.session_state: st.session_state['schichten'] = []

    tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    bereiche = ["Küche", "Service", "Spülküche", "Bar", "Overhead"]

    # Sidebar Navigation
    st.sidebar.title("👨‍🍳 GastroPro v1.7")
    if st.sidebar.button("Logout"):
        st.session_state["password_correct"] = False
        st.rerun()
    page = st.sidebar.radio("Menü:", ["📊 Dashboard", "🍲 Speisen & Getränke", "📅 Personal & Absatz-Check", "📜 Speisekarte"])

    # --- 1. DASHBOARD ---
    if page == "📊 Dashboard":
        st.header("📊 Kosten-Analyse")
        total_p = sum(s['Kosten'] for s in st.session_state['schichten'])
        c1, c2 = st.columns(2)
        c1.metric("Personal-Gesamtkosten (Woche)", f"{total_p:.2f} €")
        c2.metric("Rezepte gesamt", len(st.session_state['rezepte']))
        if st.session_state['schichten']:
            df_p = pd.DataFrame(st.session_state['schichten'])
            st.bar_chart(df_p.groupby("Bereich")["Kosten"].sum().reindex(bereiche).fillna(0))

    # --- 2. SPEISEN & GETRÄNKE (KALKULATION) ---
    elif page == "🍲 Speisen & Getränke":
        st.header("🍲 Neue Kalkulation")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name")
            kat = st.selectbox("Kategorie", ["Speise", "Getränk"])
            ek = st.number_input("Warenwert Netto (€)", min_value=0.0, value=2.50)
        with col2:
            gemeinkosten = st.slider("Gemeinkosten %", 0, 100, 25)
            vk = st.number_input("VK Brutto (€)", min_value=0.0, value=12.50)
            mwst = st.radio("MwSt (%)", [19, 7], horizontal=True)

        netto_vk = vk / (1 + mwst/100)
        selbstkosten = ek * (1 + gemeinkosten/100)
        gewinn = netto_vk - selbstkosten
        marge = (gewinn / netto_vk * 100) if netto_vk > 0 else 0

        if st.button("💾 Speichern"):
            st.session_state['rezepte'].append({"Name": name, "Kat": kat, "VK": vk, "Marge %": round(marge, 2)})
            st.success(f"{name} wurde hinzugefügt!")

    # --- 3. PERSONAL & ABSATZ-CHECK ---
    elif page == "📅 Personal & Absatz-Check":
        st.header("📅 Wochenplanung")
        t1, t2 = st.tabs(["➕ Neue Schicht", "📋 Übersicht"])
        with t1:
            c1, c2 = st.columns(2)
            with c1:
                m_tag = st.selectbox("Tag", tage); m_name = st.text_input("Name"); m_bereich = st.selectbox("Abteilung", bereiche)
            with c2:
                m_std = st.number_input("Std", value=8.0); m_lohn = st.number_input("Lohn/Std", value=15.0); u_ziel = st.number_input("Umsatz-Ziel (€)", value=1000.0)
            if st.button("Schicht speichern"):
                st.session_state['schichten'].append({"Tag": m_tag, "Name": m_name, "Bereich": m_bereich, "Kosten": m_std * m_lohn * 1.2, "Umsatz_Soll": u_ziel})
                st.success("Gespeichert!")
        with t2:
            for tag in tage:
                tag_schichten = [s for s in st.session_state['schichten'] if s['Tag'] == tag]
                with st.expander(f"📌 {tag}", expanded=True):
                    if tag_schichten:
                        t_kosten = sum(s['Kosten'] for s in tag_schichten); t_umsatz = tag_schichten[0]['Umsatz_Soll']
                        st.write(f"Kosten: {t_kosten:.2f} € | Ziel: {t_umsatz:.2f} €")
                        s_anteil = st.slider(f"Speisen %", 0, 100, 70, key=f"s_{tag}")
                        if st.session_state['rezepte']:
                            df_r = pd.DataFrame(st.session_state['rezepte'])
                            avg_s = df_r[df_r['Kat'] == "Speise"]['VK'].mean() if not df_r[df_r['Kat'] == "Speise"].empty else 0
                            avg_g = df_r[df_r['Kat'] == "Getränk"]['VK'].mean() if not df_r[df_r['Kat'] == "Getränk"].empty else 0
                            ca, cb = st.columns(2)
                            if avg_s > 0: ca.metric("Ziel Speisen", f"{int((t_umsatz * s_anteil/100) / avg_s)} Stk.")
                            if avg_g > 0: cb.metric("Ziel Getränke", f"{int((t_umsatz * (100-s_anteil)/100) / avg_g)} Stk.")
                        for i, s in enumerate(st.session_state['schichten']):
                            if s['Tag'] == tag:
                                if st.button(f"🗑️ {s['Name']}", key=f"del_p_{tag}_{i}"):
                                    st.session_state['schichten'].pop(i); st.rerun()
                    else: st.write("Keine Planung.")

    # --- 4. SPEISEKARTE (MIT EINZEL-LÖSCH-FUNKTION) ---
    elif page == "📜 Speisekarte":
        st.header("📜 Speisekarte verwalten")
        if st.session_state['rezepte']:
            # Spaltenköpfe für die manuelle Liste
            st.markdown("**Gericht / Getränk** | **Preis** | **Marge** | **Aktion**")
            # Wir nutzen eine Kopie der Liste zum Iterieren, damit das Löschen keine Index-Fehler verursacht
            for i, r in enumerate(st.session_state['rezepte']):
                col_name, col_preis, col_marge, col_del = st.columns([3, 2, 2, 1])
                col_name.write(f"{r['Name']} ({r['Kat']})")
                col_preis.write(f"{r['VK']:.2f} €")
                col_marge.write(f"{r['Marge %']}%")
                if col_del.button("🗑️", key=f"btn_del_rez_{i}"):
                    st.session_state['rezepte'].pop(i)
                    st.rerun()
            
            st.markdown("---")
            if st.button("⚠️ Komplette Karte leeren"):
                st.session_state['rezepte'] = []
                st.rerun()
        else:
            st.info("Noch keine Speisen kalkuliert.")
