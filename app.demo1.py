import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. KONFIGURATION ---
st.set_page_config(page_title="GastroPro v1.9.6 - Pro Dashboard", page_icon="📊", layout="wide")

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
        {"Name": "Wiener Schnitzel", "Kat": "Speise", "VK": 24.50, "Marge %": 68.5},
        {"Name": "Pasta Trüffel", "Kat": "Speise", "VK": 18.50, "Marge %": 75.0},
        {"Name": "Hausgemachte Limonade", "Kat": "Getränk", "VK": 5.50, "Marge %": 88.0},
        {"Name": "Gin Tonic", "Kat": "Getränk", "VK": 9.50, "Marge %": 82.5},
        {"Name": "Helles Bier", "Kat": "Getränk", "VK": 4.80, "Marge %": 85.0}
    ]
    st.session_state['schichten'] = [
        {"Tag": "Montag", "Name": "Max", "Bereich": "Küche", "Kosten": 180.0, "Umsatz_Soll": 1500.0},
        {"Tag": "Montag", "Name": "Anna", "Bereich": "Service", "Kosten": 120.0, "Umsatz_Soll": 1500.0},
        {"Tag": "Dienstag", "Name": "Lukas", "Bereich": "Bar", "Kosten": 100.0, "Umsatz_Soll": 1000.0}
    ]
    st.success("Demo-Daten geladen!")

# --- 4. HAUPTPROGRAMM ---
if check_password():
    if 'rezepte' not in st.session_state: st.session_state['rezepte'] = []
    if 'schichten' not in st.session_state: st.session_state['schichten'] = []

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

    # --- 📊 DASHBOARD (EXTENDED) ---
    if page == "📊 Dashboard":
        st.header("📊 Wochen-Analyse & Forecast")
        
        # Daten vorbereiten
        total_kosten = sum(s['Kosten'] for s in st.session_state['schichten'])
        # Wir nehmen den Umsatz-Soll pro Tag (nur einmal pro Tag zählen)
        df_schichten = pd.DataFrame(st.session_state['schichten'])
        if not df_schichten.empty:
            total_umsatz = df_schichten.drop_duplicates(subset=['Tag'])['Umsatz_Soll'].sum()
        else:
            total_umsatz = 0
            
        # KPI Zeile
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Personal-Kosten", f"{total_kosten:.2f} €")
        c2.metric("Ziel-Umsatz", f"{total_umsatz:.2f} €")
        
        p_quote = (total_kosten / total_umsatz * 100) if total_umsatz > 0 else 0
        c3.metric("Personal-Quote", f"{p_quote:.1f} %", delta="-30% Ziel", delta_color="inverse")
        c4.metric("Rezepte", len(st.session_state['rezepte']))

        st.markdown("---")
        
        # Absatz Forecast Info
        if total_umsatz > 0 and st.session_state['rezepte']:
            st.subheader("🎯 Benötigte Verkäufe für Wochenziel")
            df_r = pd.DataFrame(st.session_state['rezepte'])
            avg_s = df_r[df_r['Kat'] == "Speise"]['VK'].mean() if not df_r[df_r['Kat'] == "Speise"].empty else 0
            avg_g = df_r[df_r['Kat'] == "Getränk"]['VK'].mean() if not df_r[df_r['Kat'] == "Getränk"].empty else 0
            
            col_a, col_b = st.columns(2)
            # Annahme 60/40 Split für das Dashboard-Beispiel
            with col_a:
                if avg_s > 0:
                    st.info(f"🥗 **Speisen:** ca. **{int((total_umsatz * 0.6) / avg_s)}** Verkäufe nötig")
            with col_b:
                if avg_g > 0:
                    st.info(f"🍹 **Getränke:** ca. **{int((total_umsatz * 0.4) / avg_g)}** Verkäufe nötig")

        # Charts
        if not df_schichten.empty:
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.write("**Kosten nach Bereich**")
                st.bar_chart(df_schichten.groupby("Bereich")["Kosten"].sum().reindex(bereiche).fillna(0))
            with col_chart2:
                st.write("**Umsatz vs. Personal (Tagesvergleich)**")
                daily_data = df_schichten.groupby("Tag").agg({"Kosten": "sum", "Umsatz_Soll": "first"})
                st.line_chart(daily_data)

    # --- 🍲 KALKULATION ---
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

    # --- 📅 PERSONAL & ABSATZ ---
    elif page == "📅 Personal & Absatz":
        st.header("📅 Planung")
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
                    st.write(f"Personal: {sum(s['Kosten'] for s in tag_schichten):.2f} € | Ziel: {t_umsatz:.2f} €")
                    for i, sch in enumerate(st.session_state['schichten']):
                        if sch['Tag'] == tag:
                            col_n, col_d = st.columns([5,1])
                            col_n.write(f"• {sch['Name']} ({sch['Bereich']})")
                            if col_d.button("🗑️", key=f"del_p_{tag}_{i}"):
                                st.session_state['schichten'].pop(i)
                                st.rerun()

    # --- 📜 SPEISEKARTE ---
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
