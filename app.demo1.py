import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. KONFIGURATION ---
st.set_page_config(page_title="GastroPro v1.9.5", page_icon="👨‍🍳", layout="wide")

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

# --- 3. DEMO-DATEN ---
def load_demo_data():
    st.session_state['rezepte'] = [
        {"Name": "Wiener Schnitzel (Kalb)", "Kat": "Speise", "VK": 24.50, "Marge %": 68.5},
        {"Name": "Lachsforelle Müllerin Art", "Kat": "Speise", "VK": 21.90, "Marge %": 72.1},
        {"Name": "Trüffel Pasta", "Kat": "Speise", "VK": 18.50, "Marge %": 75.0},
        {"Name": "Rinderfilet 200g", "Kat": "Speise", "VK": 32.00, "Marge %": 62.0},
        {"Name": "Caesar Salad", "Kat": "Speise", "VK": 14.50, "Marge %": 78.0},
        {"Name": "Hausgemachte Limonade", "Kat": "Getränk", "VK": 5.50, "Marge %": 88.0},
        {"Name": "Gin Tonic (Hausmarke)", "Kat": "Getränk", "VK": 9.50, "Marge %": 82.5},
        {"Name": "Helles Bier 0,5l", "Kat": "Getränk", "VK": 4.80, "Marge %": 85.0},
        {"Name": "Aperol Spritz", "Kat": "Getränk", "VK": 7.50, "Marge %": 84.0},
        {"Name": "Espresso", "Kat": "Getränk", "VK": 2.80, "Marge %": 92.0}
    ]
    st.session_state['schichten'] = [
        {"Tag": "Montag", "Name": "Max (Küchenchef)", "Bereich": "Küche", "Kosten": 180.0, "Umsatz_Soll": 1500.0},
        {"Tag": "Montag", "Name": "Anna", "Bereich": "Service", "Kosten": 120.0, "Umsatz_Soll": 1500.0},
        {"Tag": "Dienstag", "Name": "Lukas", "Bereich": "Bar", "Kosten": 100.0, "Umsatz_Soll": 1000.0}
    ]
    st.success("Demo-Daten geladen!")

# --- 4. HAUPTPROGRAMM ---
if check_password():
    if 'rezepte' not in st.session_state: 
        st.session_state['rezepte'] = []
    if 'schichten' not in st.session_state: 
        st.session_state['schichten'] = []

    tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    bereiche = ["Küche", "Service", "Spülküche", "Bar", "Overhead"]

    st.sidebar.title("👨‍🍳 GastroPro")
    if st.sidebar.button("✨ Demo-Daten laden"):
        load_demo_data()
        st.rerun()
    if st.sidebar.button("Logout"):
        st.session_state["password_correct"] = False
        st.rerun()
    
    page = st.sidebar.radio("Menü:", ["📊 Dashboard", "🍲 Kalkulation", "📅 Personal & Absatz", "📜 Speisekarte"])

    if page == "📊 Dashboard":
        st.header("📊 Kosten-Analyse")
        total_p = sum(s['Kosten'] for s in st.session_state['schichten'])
        c1, c2 = st.columns(2)
        c1.metric("Personal-Kosten (Woche)", f"{total_p:.2f} €")
        c2.metric("Rezepte gesamt", len(st.session_state['rezepte']))
        if st.session_state['schichten']:
            df_p = pd.DataFrame(st.session_state['schichten'])
            st.bar_chart(df_p.groupby("Bereich")["Kosten"].sum().reindex(bereiche).fillna(0))

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
            st.success("Gespeichert!")

    elif page == "📅 Personal & Absatz":
        st.header("📅 Wochenplanung & Absatz-Check")
        with st.expander("➕ Neue Schicht hinzufügen"):
            c1, c2 = st.columns(2)
            with c1:
                t = st.selectbox("Wochentag", tage); n = st.text_input("Name"); b = st.selectbox("Bereich", bereiche)
            with c2:
                s = st.number_input("Stunden", value=8.0); l = st.number_input("Lohn", value=15.0); u = st.number_input("Tagesumsatz Ziel (€)", value=1000.0)
            if st.button("Schicht eintragen"):
                st.session_state['schichten'].append({"Tag": t, "Name": n, "Bereich": b, "Kosten": s*l*1.2, "Umsatz_Soll": u})
                st.rerun()

        for tag in tage:
            tag_schichten = [s for s in st.session_state['schichten'] if s['Tag'] == tag]
            if tag_schichten:
                with st.expander(f"📌 {tag}", expanded=True):
                    t_umsatz = tag_schichten[0]['Umsatz_Soll']
                    st.write(f"**Personal:** {sum(s['Kosten'] for s in tag_schichten):.2f} € | **Ziel:** {t_umsatz:.2f} €")
                    
                    if st.session_state['rezepte']:
                        df_r = pd.DataFrame(st.session_state['rezepte'])
                        avg_s = df_r[df_r['Kat'] == "Speise"]['VK'].mean() if not df_r[df_r['Kat'] == "Speise"].empty else 0
                        avg_g = df_r[df_r['Kat'] == "Getränk"]['VK'].mean() if not df_r[df_r['Kat'] == "Getränk"].empty else 0
                        split = st.slider(f"Mix % (Speisen vs. Getränke)", 0, 100, 60, key=f"split_{tag}")
                        
                        c_a, c_b = st.columns(2)
                        if avg_s > 0:
                            s_ziel = (t_umsatz * (split/100)) / avg_s
                            c_a.metric("Speisen", f"{int(s_ziel)} Stk.", f"Ø {avg_s:.2f} €")
                        if avg_g > 0:
                            g_ziel = (t_umsatz * ((100-split)/100)) / avg_g
                            # --- ZEILE 135 FIX ---
                            c_b.metric("Getränke", f"{int(g_ziel)} Stk.", f"Ø {avg_g:.2f} €")
                    
                    for i, sch in enumerate(st.session_state['schichten']):
                        if sch['Tag'] == tag:
                            col_n, col_d = st.columns([5,1])
                            col_n.write(f"• {sch['Name']} ({sch['Bereich']})")
                            if col_d.button("🗑️", key=f"del_p_{tag}_{i}"):
                                st.session_state['schichten'].pop(i)
                                st.rerun()

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
