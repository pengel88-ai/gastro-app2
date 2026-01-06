import streamlit as st
import pandas as pd

# Seiteneinstellungen
st.set_page_config(page_title="GastroPro v3 - Personal & Kalkulation", page_icon="👨‍🍳", layout="wide")

# --- PASSWORT SICHERHEIT ---
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔐 GastroPro Login")
        password = st.text_input("Passwort eingeben", type="password")
        if st.button("Anmelden"):
            if password == "Gastro2024": # Hier dein Passwort ändern
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

    # --- NAVIGATION ---
    st.sidebar.title("👨‍🍳 GastroPro v3")
    page = st.sidebar.radio("Menü", ["Dashboard", "Speisen-Kalkulation", "Personal-Planer"])

    # --- 1. PERSONAL-PLANER (NEU) ---
    if page == "Personal-Planer":
        st.header("📅 Personalplanung & Kosten-Check")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Schicht-Eingabe")
            mitarbeiter = st.text_input("Name Mitarbeiter")
            rolle = st.selectbox("Rolle", ["Küche", "Service", "Bar", "Reinigung"])
            stunden = st.number_input("Stunden", min_value=1.0, max_value=15.0, value=8.0)
            lohn = st.number_input("Stundenlohn Brutto (€)", min_value=12.41, value=15.0)
            
            if st.button("Schicht hinzufügen"):
                kosten = stunden * lohn * 1.2 # 20% Lohnnebenkosten Pauschale
                st.session_state['schichten'].append({
                    "Name": mitarbeiter, "Rolle": rolle, "Stunden": stunden, "Kosten": kosten
                })
                st.success(f"Schicht für {mitarbeiter} gespeichert.")

        with col2:
            st.subheader("Tages-Analyse")
            umsatz_soll = st.number_input("Erwarteter Tagesumsatz (€)", min_value=1.0, value=1000.0)
            
            if st.session_state['schichten']:
                df_schichten = pd.DataFrame(st.session_state['schichten'])
                st.table(df_schichten)
                
                total_personal = df_schichten["Kosten"].sum()
                quote = (total_personal / umsatz_soll) * 100
                
                st.markdown("---")
                c1, c2 = st.columns(2)
                c1.metric("Gesamtkosten Personal", f"{total_personal:.2f} €")
                
                if quote > 35:
                    c2.error(f"Personalquote: {quote:.1f}% (ZU HOCH!)")
                    st.warning("⚠️ Dein Personal ist zu teuer für diesen Umsatz. Reduziere die Stunden oder erhöhe das Umsatz-Ziel.")
                else:
                    c2.success(f"Personalquote: {quote:.1f}% (Optimal)")
            else:
                st.info("Noch keine Schichten für heute geplant.")
# --- EXPORT FUNKTION FÜR DIENSTPLAN ---
if st.session_state['schichten']:
    df_personal = pd.DataFrame(st.session_state['schichten'])
    
    csv_p = df_personal.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Dienstplan als CSV exportieren",
        data=csv_p,
        file_name='dienstplan_heute.csv',
        mime='text/csv',
    )

    # --- 2. SPEISEN-KALKULATION ---
    elif page == "Speisen-Kalkulation":
        st.header("🍲 Speisenkalkulation")
        # (Hier bleibt dein bisheriger Kalkulations-Code...)
        name = st.text_input("Name des Gerichts")
        ek = st.number_input("Wareneinsatz (€)", value=5.0)
        vk = st.number_input("Verkaufspreis Brutto (€)", value=20.0)
        if st.button("Speichern"):
            st.session_state['rezepte'].append({"Name": name, "VK": vk, "EK": ek})
            st.success("Gericht gespeichert!")

    # --- 3. DASHBOARD ---
    elif page == "Dashboard":
        st.header("📈 Dashboard: Alles auf einen Blick")
        
        # Berechnung für das Dashboard
        total_p_kosten = sum(s['Kosten'] for s in st.session_state['schichten'])
        anzahl_rezepte = len(st.session_state['rezepte'])
        
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Personalkosten Heute", f"{total_p_kosten:.2f} €")
        kpi2.metric("Rezepte in Datenbank", anzahl_rezepte)
        kpi3.metric("Status", "Aktiv")

        # Visuelle Darstellung
        if st.session_state['schichten']:
            st.subheader("Kostenverteilung nach Rollen")
            df_plot = pd.DataFrame(st.session_state['schichten'])
            st.bar_chart(df_plot.groupby("Rolle")["Kosten"].sum())
