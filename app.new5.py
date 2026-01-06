import streamlit as st
import pandas as pd
from datetime import datetime

# --- KONFIGURATION ---
st.set_page_config(page_title="GastroPro v1.2 - Wochenplaner", page_icon="👨‍🍳", layout="wide")

# --- PASSWORT SICHERHEIT ---
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔐 GastroPro Login")
        password = st.text_input("Bitte Passwort eingeben", type="password")
        if st.button("Anmelden"):
            if password == "Gastro2026": # Dein Passwort
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Passwort falsch.")
        return False
    return True

if check_password():

    # --- DATENSPEICHER ---
    if 'rezepte' not in st.session_state: st.session_state['rezepte'] = []
    if 'schichten' not in st.session_state: st.session_state['schichten'] = []

    # --- WOCHENTAGE DEFINITION ---
    tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("👨‍🍳 GastroPro v1.2")
    page = st.sidebar.radio("Menü wählen:", ["📊 Dashboard", "🍲 Speisen-Kalkulation", "📅 Personal-Wochenplaner", "📜 Meine Speisekarte"])
    
    if st.sidebar.button("Logout"):
        st.session_state["password_correct"] = False
        st.rerun()

    # --- 1. DASHBOARD ---
    if page == "📊 Dashboard":
        st.header("📈 Dashboard")
        total_p_kosten = sum(s['Kosten'] for s in st.session_state['schichten'])
        anzahl_rezepte = len(st.session_state['rezepte'])
        
        col1, col2 = st.columns(2)
        col1.metric("Gesamte Personalkosten (Woche)", f"{total_p_kosten:.2f} €")
        col2.metric("Anzahl Rezepte", anzahl_rezepte)

        if st.session_state['schichten']:
            st.subheader("Personalkosten nach Wochentag")
            df_p = pd.DataFrame(st.session_state['schichten'])
            # Sortierung nach Wochentagen sicherstellen
            kosten_pro_tag = df_p.groupby("Tag")["Kosten"].sum().reindex(tage).fillna(0)
            st.bar_chart(kosten_pro_tag)

    # --- 2. SPEISEN-KALKULATION ---
    elif page == "🍲 Speisen-Kalkulation":
        st.header("🍲 Neue Speise kalkulieren")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name des Gerichts")
            kategorie = st.selectbox("Kategorie", ["Vorspeise", "Hauptgang", "Dessert", "Getränk"])
            wareneinsatz = st.number_input("Warenwert Netto (€)", min_value=0.0, value=2.0)
        with col2:
            gemeinkosten = st.slider("Gemeinkosten %", 0, 100, 25)
            ziel_preis = st.number_input("Verkaufspreis Brutto (€)", min_value=0.0, value=10.0)
            mwst = st.radio("MwSt", [19, 7], horizontal=True)

        selbstkosten = (wareneinsatz + 0.20) * (1 + gemeinkosten/100)
        netto_vk = ziel_preis / (1 + mwst/100)
        gewinn = netto_vk - selbstkosten
        marge = (gewinn / netto_vk * 100) if netto_vk > 0 else 0

        if st.button("Speichern"):
            st.session_state['rezepte'].append({
                "Name": name, "Kategorie": kategorie, "EK": wareneinsatz, 
                "VK": ziel_preis, "Marge %": round(marge, 2)
            })
            st.success("Gericht gespeichert!")

    # --- 3. PERSONAL-WOCHENPLANER ---
    elif page == "📅 Personal-Wochenplaner":
        st.header("📅 Wochen-Einsatzplan")
        
        tab_einplanung, tab_uebersicht = st.tabs(["➕ Schicht planen", "📋 Wochenübersicht"])
        
        with tab_einplanung:
            col1, col2 = st.columns(2)
            with col1:
                m_tag = st.selectbox("Wochentag", tage)
                m_name = st.text_input("Mitarbeiter Name")
                m_rolle = st.selectbox("Bereich", ["Küche", "Service", "Bar", "Spülküche"])
            with col2:
                m_stunden = st.number_input("Arbeitsstunden", value=8.0, step=0.5)
                m_lohn = st.number_input("Stundenlohn (€)", value=15.0)
                umsatz_erwartet = st.number_input("Erwarteter Umsatz für diesen Tag (€)", value=1000.0)

            if st.button("Schicht für " + m_tag + " speichern"):
                kosten = m_stunden * m_lohn * 1.2
                st.session_state['schichten'].append({
                    "Tag": m_tag, "Name": m_name, "Bereich": m_rolle, 
                    "Std": m_stunden, "Kosten": kosten, "Umsatz_Soll": umsatz_erwartet
                })
                st.success(f"Eingetragen: {m_name} am {m_tag}")

        with tab_uebersicht:
            for tag in tage:
                schichten_tag = [s for s in st.session_state['schichten'] if s['Tag'] == tag]
                
                with st.expander(f"📌 {tag}", expanded=True):
                    if schichten_tag:
                        # Berechnungen für den Tag
                        tages_kosten = sum(s['Kosten'] for s in schichten_tag)
                        tages_umsatz = schichten_tag[0]['Umsatz_Soll'] # Nimmt den Wert der ersten Schicht
                        quote = (tages_kosten / tages_umsatz * 100) if tages_umsatz > 0 else 0
                        
                        col_a, col_b, col_c = st.columns([3, 1, 1])
                        col_a.write(f"**Gesamtkosten Personal:** {tages_kosten:.2f} € | **Ziel-Umsatz:** {tages_umsatz:.2f} €")
                        
                        if quote > 35:
                            col_b.error(f"Quote: {quote:.1f}%")
                        else:
                            col_b.success(f"Quote: {quote:.1f}%")
                        
                        # Lösch-Funktion innerhalb des Tages
                        for i, s in enumerate(st.session_state['schichten']):
                            if s['Tag'] == tag:
                                c1, c2, c3 = st.columns([3, 2, 1])
                                c1.write(f"• {s['Name']} ({s['Bereich']}) - {s['Std']} Std.")
                                if c3.button("🗑️", key=f"del_p_{tag}_{i}"):
                                    st.session_state['schichten'].pop(i)
                                    st.rerun()
                    else:
                        st.write("*Keine Schichten geplant*")

    # --- 4. MEINE SPEISEKARTE ---
    elif page == "📜 Meine Speisekarte":
        st.header("📜 Speisekarte verwalten")
        if st.session_state['rezepte']:
            for i, rez in enumerate(st.session_state['rezepte']):
                with st.container():
                    c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
                    c1.write(f"**{rez['Name']}** ({rez['Kategorie']})")
                    c2.write(f"VK: {rez['VK']:.2f} €")
                    c3.write(f"Marge: {rez['Marge %']}%")
                    if c4.button("🗑️", key=f"del_r_{i}"):
                        st.session_state['rezepte'].pop(i)
                        st.rerun()
            
            st.markdown("---")
            df_r = pd.DataFrame(st.session_state['rezepte'])
            csv_r = df_r.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Speisekarte Download", csv_r, "speisekarte.csv", "text/csv")
        else:
            st.info("Keine Gerichte vorhanden.")
