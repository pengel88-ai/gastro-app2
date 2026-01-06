import streamlit as st
import pandas as pd

# Seiteneinstellungen
st.set_page_config(page_title="GastroPro v2 - Secure", page_icon="🔐")

# --- PASSWORT SICHERHEIT ---
def check_password():
    """Gibt True zurück, wenn der Benutzer das korrekte Passwort eingegeben hat."""

    def password_entered():
        """Überprüft, ob das eingegebene Passwort korrekt ist."""
        # Ersetze 'dein-sicheres-passwort' durch dein tatsächliches Wunsch-Passwort
        if st.session_state["password"] == "Gastro2024": 
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Passwort aus dem Speicher löschen
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Erstmalige Anzeige des Login-Feldes
        st.title("🔐 GastroPro Login")
        st.text_input(
            "Bitte gib das Passwort ein, um fortzufahren:",
            type="password",
            on_change=password_entered,
            key="password",
        )
        st.info("Hinweis: Dies ist eine geschützte Anwendung für Gastronomen.")
        return False
    elif not st.session_state["password_correct"]:
        # Passwort war falsch
        st.title("🔐 GastroPro Login")
        st.text_input(
            "Bitte gib das Passwort ein, um fortzufahren:",
            type="password",
            on_change=password_entered,
            key="password",
        )
        st.error("❌ Passwort falsch. Bitte erneut versuchen.")
        return False
    else:
        # Passwort korrekt
        return True

# --- APP STARTEN, WENN LOGIN ERFOLGREICH ---
if check_password():

    # --- DATENSPEICHER (Session State) ---
    if 'rezepte' not in st.session_state:
        st.session_state['rezepte'] = []

    # --- NAVIGATION ---
    st.sidebar.title("👨‍🍳 GastroPro")
    st.sidebar.write(f"Angemeldet als: **Admin**")
    if st.sidebar.button("Logout"):
        st.session_state["password_correct"] = False
        st.rerun()

    page = st.sidebar.radio("Menü", ["Dashboard", "Kalkulations-Tool", "Meine Speisekarte"])

    # --- 1. KALKULATIONS-TOOL ---
    if page == "Kalkulations-Tool":
        st.header("🍲 Speisenkalkulation")
        
        with st.expander("Gerichts-Details", expanded=True):
            name = st.text_input("Name des Gerichts")
            kategorie = st.selectbox("Kategorie", ["Vorspeise", "Hauptspeise", "Dessert", "Getränk"])

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Kostenanalyse")
            wareneinsatz = st.number_input("Warenwert Netto (€)", min_value=0.0, step=0.50, value=0.0)
            gemeinkosten = st.slider("Gemeinkosten-Aufschlag %", 0, 100, 20)
            gewuerz_pauschale = st.number_input("Gewürz-Pauschale (€)", 0.0, 2.0, 0.20)
        
        selbstkosten = (wareneinsatz + gewuerz_pauschale) * (1 + gemeinkosten/100)
        
        with col2:
            st.subheader("Verkauf")
            ziel_preis = st.number_input("VK-Preis Brutto (€)", min_value=0.0, step=0.50, value=0.0)
            mwst = st.radio("MwSt.-Satz", [19, 7], horizontal=True)

        netto_verkauf = ziel_preis / (1 + mwst/100)
        gewinn_euro = netto_verkauf - selbstkosten
        marge_prozent = (gewinn_euro / netto_verkauf * 100) if netto_verkauf > 0 else 0

        st.markdown("---")
        
        # Ergebnisanzeige in Containern
        res_col1, res_col2 = st.columns(2)
        res_col1.metric("Gewinn pro Teller", f"{gewinn_euro:.2f} €")
        
        if marge_prozent < 65:
            res_col2.error(f"Marge: {marge_prozent:.1f}%")
        else:
            res_col2.success(f"Marge: {marge_prozent:.1f}%")

        if st.button("In Karte speichern"):
            if name != "" and ziel_preis > 0:
                neues_rezept = {"Name": name, "Kategorie": kategorie, "EK": f"{wareneinsatz:.2f}€", "VK": f"{ziel_preis:.2f}€", "Marge %": round(marge_prozent, 2)}
                st.session_state['rezepte'].append(neues_rezept)
                st.success(f"'{name}' wurde gespeichert!")
            else:
                st.warning("Bitte Name und Preis eingeben.")

    # --- 2. MEINE SPEISEKARTE ---
    elif page == "Meine Speisekarte":
        st.header("📜 Kalkulierte Gerichte")
        if st.session_state['rezepte']:
            df = pd.DataFrame(st.session_state['rezepte'])
            st.dataframe(df, use_container_width=True)
            
            if st.button("Liste leeren"):
                st.session_state['rezepte'] = []
                st.rerun()
        else:
            st.info("Noch keine Daten vorhanden.")

    # --- 3. DASHBOARD ---
    elif page == "Dashboard":
        st.header("📈 Dashboard")
        st.write("Willkommen im geschützten Bereich.")
        
        # Beispiel für visuelle Daten
        kpi1, kpi2 = st.columns(2)
        kpi1.metric("Anzahl Rezepte", len(st.session_state['rezepte']))
        kpi2.metric("Status", "Bereit")
        
        if len(st.session_state['rezepte']) > 0:
            df_plot = pd.DataFrame(st.session_state['rezepte'])
            st.bar_chart(df_plot.set_index("Name")["Marge %"])
