import streamlit as st
import pandas as pd
from datetime import datetime

# --- KONFIGURATION ---
st.set_page_config(page_title="GastroPro - All-in-One", page_icon="👨‍🍳", layout="wide")

# --- PASSWORT SICHERHEIT ---
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔐 GastroPro Login")
        st.write("Willkommen bei deiner Management-Zentrale.")
        password = st.text_input("Bitte Passwort eingeben", type="password")
        if st.button("Anmelden"):
            if password == "Gastro2026": # ÄNDERE MICH!
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Passwort falsch.")
        return False
    return True

# --- APP STARTET NUR BEI LOGIN ---
if check_password():

    # --- DATENSPEICHER (Session State) ---
    if 'rezepte' not in st.session_state: st.session_state['rezepte'] = []
    if 'schichten' not in st.session_state: st.session_state['schichten'] = []

    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("👨‍🍳 GastroPro v1.0")
    page = st.sidebar.radio("Menü wählen:", ["📊 Dashboard", "🍲 Speisen-Kalkulation", "📅 Personal-Planer", "📜 Meine Speisekarte"])
    
    if st.sidebar.button("Logout"):
        st.session_state["password_correct"] = False
        st.rerun()

    # --- 1. DASHBOARD ---
    if page == "📊 Dashboard":
        st.header("📈 Tages-Übersicht")
        
        # Berechnungen
        total_p_kosten = sum(s['Kosten'] for s in st.session_state['schichten'])
        anzahl_rezepte = len(st.session_state['rezepte'])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Personalkosten (geplant)", f"{total_p_kosten:.2f} €")
        col2.metric("Anzahl Rezepte", anzahl_rezepte)
        col3.metric("Datum", datetime.now().strftime("%d.%m.%Y"))

        st.markdown("---")
        if st.session_state['rezepte']:
            st.subheader("Margen-Vergleich der Speisen")
            df_rezepte = pd.DataFrame(st.session_state['rezepte'])
            st.bar_chart(df_rezepte.set_index("Name")["Marge %"])
        else:
            st.info("Noch keine Daten für Grafiken vorhanden. Kalkuliere dein erstes Gericht!")

    # --- 2. SPEISEN-KALKULATION ---
    elif page == "🍲 Speisen-Kalkulation":
        st.header("🍲 Neue Speise kalkulieren")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name des Gerichts (z.B. Pasta Carbonara)")
            kategorie = st.selectbox("Kategorie", ["Vorspeise", "Hauptgang", "Dessert", "Getränk"])
            wareneinsatz = st.number_input("Warenwert Netto (€)", min_value=0.0, step=0.10, value=2.0)
            gewuerz_p = st.number_input("Gewürzpauschale (€)", value=0.20)
        
        with col2:
            gemeinkosten = st.slider("Gemeinkosten-Aufschlag %", 0, 100, 25)
            ziel_preis = st.number_input("Verkaufspreis Brutto (€)", min_value=0.0, step=0.50, value=10.0)
            mwst = st.radio("MwSt.-Satz", [19, 7], horizontal=True)

        # Logik
        selbstkosten = (wareneinsatz + gewuerz_p) * (1 + gemeinkosten/100)
        netto_verkauf = ziel_preis / (1 + mwst/100)
        gewinn = netto_verkauf - selbstkosten
        marge = (gewinn / netto_verkauf * 100) if netto_verkauf > 0 else 0

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Selbstkosten", f"{selbstkosten:.2f} €")
        c2.metric("Gewinn/Teller", f"{gewinn:.2f} €")
        
        if marge < 65:
            c3.error(f"Marge: {marge:.1f}%")
        else:
            c3.success(f"Marge: {marge:.1f}%")

        if st.button("Gericht Speichern"):
            st.session_state['rezepte'].append({
                "Name": name, "Kategorie": kategorie, "EK": wareneinsatz, 
                "VK": ziel_preis, "Marge %": round(marge, 2)
            })
            st.success("Erfolgreich gespeichert!")

    # --- 3. PERSONAL-PLANER ---
    elif page == "📅 Personal-Planer":
        st.header("📅 Schichtplanung & Quote")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("Schicht hinzufügen")
            m_name = st.text_input("Mitarbeiter Name")
            m_rolle = st.selectbox("Bereich", ["Küche", "Service", "Bar"])
            m_stunden = st.number_input("Stunden", value=8.0)
            m_lohn = st.number_input("Lohn/Std (€)", value=15.0)
            
            if st.button("Hinzufügen"):
                kosten = m_stunden * m_lohn * 1.2 # Inkl. 20% Lohnnebenkosten
                st.session_state['schichten'].append({
                    "Name": m_name, "Bereich": m_rolle, "Std": m_stunden, "Kosten": kosten
                })

        with col2:
            st.subheader("Personal-Analyse")
            umsatz_target = st.number_input("Ziel-Umsatz heute (€)", value=1000.0)
            
            if st.session_state['schichten']:
                df_p = pd.DataFrame(st.session_state['schichten'])
                st.table(df_p)
                
                summe_p = df_p["Kosten"].sum()
                quote = (summe_p / umsatz_target) * 100
                
                st.metric("Personalkosten Gesamt", f"{summe_p:.2f} €")
                if quote > 35:
                    st.error(f"Quote: {quote:.1f}% - ZU HOCH!")
                else:
                    st.success(f"Quote: {quote:.1f}% - OK")
                
                # CSV EXPORT PERSONAL
                csv_p = df_p.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Dienstplan Download", csv_p, "dienstplan.csv", "text/csv")

    # --- 4. MEINE SPEISEKARTE ---
    elif page == "📜 Meine Speisekarte":
        st.header("📜 Alle kalkulierten Speisen")
        if st.session_state['rezepte']:
            df_r = pd.DataFrame(st.session_state['rezepte'])
            st.dataframe(df_r, use_container_width=True)
            
            # CSV EXPORT REZEPTE
            csv_r = df_r.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Speisekarte Download", csv_r, "speisekarte.csv", "text/csv")
            
            if st.button("Alle Daten löschen"):
                st.session_state['rezepte'] = []
                st.rerun()
        else:
            st.info("Noch keine Rezepte gespeichert.")
