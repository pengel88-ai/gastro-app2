import streamlit as st
import pandas as pd

# --- 1. SETTINGS ---
st.set_page_config(page_title="GastroPro v2.1", layout="wide")

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
    # Speisen
    s1 = {"Name": "Rinder Carpaccio", "Kat": "Vorspeise", "VK": 14.5, "M": 70}
    s2 = {"Name": "Gebackener Feta", "Kat": "Vorspeise", "VK": 9.8, "M": 75}
    s3 = {"Name": "Tomatensuppe", "Kat": "Vorspeise", "VK": 7.5, "M": 82}
    s4 = {"Name": "Zwiebelrostbraten", "Kat": "Hauptgang", "VK": 28.5, "M": 64}
    s5 = {"Name": "Lachs-Filet", "Kat": "Hauptgang", "VK": 24.9, "M": 68}
    s6 = {"Name": "Vegane Bowl", "Kat": "Hauptgang", "VK": 16.5, "M": 78}
    s7 = {"Name": "Apfelstrudel", "Kat": "Dessert", "VK": 7.9, "M": 74}
    s8 = {"Name": "Crème Brûlée", "Kat": "Dessert", "VK": 8.5, "M": 77}
    
    # Getränke
    g1 = {"Name": "Grauburgunder", "Kat": "Wein", "VK": 7.5, "M": 80}
    g2 = {"Name": "Pils 0,5l", "Kat": "Bier", "VK": 4.9, "M": 85}
    g3 = {"Name": "Cola 0,4l", "Kat": "AFG", "VK": 4.5, "M": 88}
    g4 = {"Name": "Moscow Mule", "Kat": "Cocktails", "VK": 11.0, "M": 81}
    g5 = {"Name": "Cappuccino", "Kat": "Heißgetränke", "VK": 4.2, "M": 89}
    
    st.session_state['rezepte'] = [s1, s2, s3, s4, s5, s6, s7, s8, g1, g2, g3, g4, g5]

    # Personal (6 Mitarbeiter)
    p1 = {"Tag": "Mo", "Name": "Thomas", "Bereich": "Küche", "Kosten": 190, "Ziel": 2000}
    p2 = {"Tag": "Mo", "Name": "Stefan", "Bereich": "Küche", "Kosten": 160, "Ziel": 2000}
    p3 = {"Tag": "Mo", "Name": "Sarah", "Bereich": "Service", "Kosten": 130, "Ziel": 2000}
    p4 = {"Tag": "Mo", "Name": "Julia", "Bereich": "Service", "Kosten": 120, "Ziel": 2000}
    p5 = {"Tag": "Mo", "Name": "Lukas", "Bereich": "Bar", "Kosten": 110, "Ziel": 2000}
    p6 = {"Tag": "Mo", "Name": "Kevin", "Bereich": "Spüle", "Kosten": 90, "Ziel": 2000}
    
    st.session_state['schichten'] = [p1, p2, p3, p4, p5, p6]
    st.success("Show-Daten erfolgreich geladen!")

# --- 4. HAUPT APP ---
if check_password():
    if 'rezepte' not in st.session_state: st.session_state['rezepte'] = []
    if 'schichten' not in st.session_state: st.session_state['schichten'] = []

    st.sidebar.title("👨‍🍳 GastroPro")
    if st.sidebar.button("✨ Demo-Daten laden"):
        load_demo()
        st.rerun()
    
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📅 Personalplanung", "📜 Speisekarte"])

    with tab1:
        st.header("📊 Wochen-Analyse")
        if st.session_state['schichten']:
            df = pd.DataFrame(st.session_state['schichten'])
            c1, c2, c3 = st.columns(3)
            kosten = df['Kosten'].sum()
            ziel = df['Ziel'].iloc[0]
            c1.metric("Personal-Kosten", f"{kosten:.2f} €")
            c2.metric("Umsatz-Ziel", f"{ziel:.2f} €")
            c3.metric("Quote", f"{(kosten/ziel*100):.1f} %")
            st.write("---")
            st.write("**Kosten nach Abteilung**")
            st.bar_chart(df.groupby("Bereich")["Kosten"].sum())
        else:
            st.warning("Bitte Demo-Daten in der Sidebar laden.")

    with tab2:
        st.header("📅 Mitarbeiter heute")
        if st.session_state['schichten']:
            for s in st.session_state['schichten']:
                st.write(f"🟢 **{s['Name']}** | Bereich: {s['Bereich']} | Kosten: {s['Kosten']}€")

    with tab3:
        st.header("📜 Karte")
        if st.session_state['rezepte']:
            df_r = pd.DataFrame(st.session_state['rezepte'])
            for k in df_r['Kat'].unique():
                with st.expander(f"{k}"):
                    for _, r in df_r[df_r['Kat']==k].iterrows():
                        st.write(f"**{r['Name']}** : {r['VK']:.2f} €")
