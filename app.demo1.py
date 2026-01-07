import streamlit as st
import pandas as pd

# --- 1. SETTINGS ---
st.set_page_config(page_title="GastroPro v2.2", layout="wide", page_icon="👨‍🍳")

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
    st.session_state['rezepte'] = [
        {"Name": "Rinder Carpaccio", "Kat": "Vorspeise", "VK": 14.50, "EK": 4.20, "M": 70.0},
        {"Name": "Zwiebelrostbraten", "Kat": "Hauptgang", "VK": 28.50, "EK": 9.50, "M": 64.0},
        {"Name": "Apfelstrudel", "Kat": "Dessert", "VK": 7.90, "EK": 1.80, "M": 74.0},
        {"Name": "Grauburgunder", "Kat": "Wein", "VK": 7.50, "EK": 1.50, "M": 80.0},
        {"Name": "Pils 0,5l", "Kat": "Bier", "VK": 4.90, "EK": 0.80, "M": 85.0}
    ]
    st.session_state['schichten'] = [
        {"Tag": "Mo", "Name": "Thomas", "Bereich": "Küche", "Kosten": 190.0, "Ziel": 2000.0},
        {"Tag": "Mo", "Name": "Sarah", "Bereich": "Service", "Kosten": 130.0, "Ziel": 2000.0}
    ]
    st.success("Demo-Daten geladen!")

# --- 4. HAUPT APP ---
if check_password():
    if 'rezepte' not in st.session_state: st.session_state['rezepte'] = []
    if 'schichten' not in st.session_state: st.session_state['schichten'] = []

    kats = ["Vorspeise", "Hauptgang", "Dessert", "Wein", "Bier", "AFG", "Cocktails", "Heißgetränke"]
    bereiche = ["Küche", "Service", "Bar", "Spülküche", "Overhead"]

    st.sidebar.title("👨‍🍳 GastroPro")
    if st.sidebar.button("✨ Demo-Daten laden"):
        load_demo()
        st.rerun()
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🍲 Kalkulation", "📅 Personal", "📜 Speisekarte"])

    # --- TAB 1: DASHBOARD ---
    with tab1:
        st.header("📊 Wochen-Analyse")
        if st.session_state['schichten']:
            df = pd.DataFrame(st.session_state['schichten'])
            kosten = df['Kosten'].sum()
            # Ziel vom ersten Eintrag nehmen oder 0
            ziel = df['Ziel'].iloc[0] if not df.empty else 1
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Personal-Kosten", f"{kosten:.2f} €")
            c2.metric("Umsatz-Ziel", f"{ziel:.2f} €")
            quote = (kosten/ziel*100)
            c3.metric("Personal-Quote", f"{quote:.1f} %", delta="-30% Ziel", delta_color="inverse")
            
            st.write("---")
            st.bar_chart(df.groupby("Bereich")["Kosten"].sum())
        else:
            st.info("Noch keine Daten vorhanden. Nutze die Demo oder die Reiter.")

    # --- TAB 2: KALKULATION ---
    with tab2:
        st.header("🍲 Neue Rezeptur kalkulieren")
        with st.form("form_kalk"):
            col1, col2 = st.columns(2)
            with col1:
                n_name = st.text_input("Name des Artikels")
                n_kat = st.selectbox("Kategorie", kats)
            with col2:
                n_ek = st.number_input("EK Netto (€)", min_value=0.0, value=2.0)
                n_vk = st.number_input("VK Brutto (€)", min_value=0.0, value=10.0)
            
            if st.form_submit_button("In Speisekarte speichern"):
                # Berechnung Marge (vereinfacht 19% MwSt)
                netto_vk = n_vk / 1.19
                marge = ((netto_vk - n_ek) / netto_vk * 100) if netto_vk > 0 else 0
                st.session_state['rezepte'].append({
                    "Name": n_name, "Kat": n_kat, "VK": n_vk, "EK": n_ek, "M": round(marge, 1)
                })
                st.success(f"{n_name} gespeichert!")

    # --- TAB 3: PERSONALPLANUNG ---
    with tab3:
        st.header("📅 Schichtplan erstellen")
        with st.expander("➕ Neue Schicht hinzufügen"):
            with st.form("form_pers"):
                c1, c2, c3 = st.columns(3)
                p_name = c1.text_input("Mitarbeiter Name")
                p_ber = c2.selectbox("Bereich", bereiche)
                p_tag = c3.selectbox("Tag", ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"])
                
                c4, c5 = st.columns(2)
                p_stunden = c4.number_input("Stunden", value=8.0)
                p_lohn = c5.number_input("Lohn/Std", value=15.0)
                
                if st.form_submit_button("Schicht speichern"):
                    p_kosten = p_stunden * p_lohn * 1.2 # inkl. Lohnnebenkosten
                    # Falls noch kein Ziel existiert, Standard 2000€
                    ziel_alt = st.session_state['schichten'][0]['Ziel'] if st.session_state['schichten'] else 2000.0
                    st.session_state['schichten'].append({
                        "Tag": p_tag, "Name": p_name, "Bereich": p_ber, "Kosten": p_kosten, "Ziel": ziel_alt
                    })
                    st.rerun()

        if st.session_state['schichten']:
            st.write("**Aktuelle Planung:**")
            st.table(pd.DataFrame(st.session_state['schichten'])[["Tag", "Name", "Bereich", "Kosten"]])

    # --- TAB 4: SPEISEKARTE ---
    with tab4:
        st.header("📜 Aktuelle Speisekarte")
        if st.session_state['rezepte']:
            df_r = pd.DataFrame(st.session_state['rezepte'])
            for k in df_r['Kat'].unique():
                with st.expander(f"{k}"):
                    for i, r in df_r[df_r['Kat']==k].iterrows():
                        col_a, col_b, col_c = st.columns([3, 1, 1])
                        col_a.write(f"**{r['Name']}**")
                        col_b.write(f"{r['VK']:.2f} €")
                        col_c.write(f"Marge: {r['M']}%")
        else:
            st.info("Die Karte ist noch leer.")
