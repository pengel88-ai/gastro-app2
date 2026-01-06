import streamlit as st
import pandas as pd
from datetime import datetime

# --- KONFIGURATION ---
st.set_page_config(page_title="GastroPro v1.4", page_icon="👨‍🍳", layout="wide")

# --- PASSWORT SICHERHEIT ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if not st.session_state["password_correct"]:
        st.title("🔐 GastroPro Login")
        password = st.text_input("Passwort eingeben", type="password")
        if st.button("Anmelden"):
            if password == "Gastro2026": 
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

    tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

    # --- SIDEBAR ---
    st.sidebar.title("👨‍🍳 GastroPro v1.4")
    if st.sidebar.button("Logout"):
        st.session_state["password_correct"] = False
        st.rerun()
    page = st.sidebar.radio("Menü:", ["📊 Dashboard", "🍲 Speisen-Kalkulation", "📅 Personal & Absatz-Check", "📜 Meine Speisekarte"])

    # --- 1. DASHBOARD ---
    if page == "📊 Dashboard":
        st.header("📈 Dashboard")
        total_p_kosten = sum(s['Kosten'] for s in st.session_state['schichten'])
        col1, col2 = st.columns(2)
        col1.metric("Personal-Budget (Woche)", f"{total_p_kosten:.2f} €")
        col2.metric("Rezepte gesamt", len(st.session_state['rezepte']))
        if st.session_state['schichten']:
            df_p = pd.DataFrame(st.session_state['schichten'])
            kosten_pro_tag = df_p.groupby("Tag")["Kosten"].sum().reindex(tage).fillna(0)
            st.bar_chart(kosten_pro_tag)

    # --- 2. SPEISEN-KALKULATION ---
    elif page == "🍲 Speisen-Kalkulation":
        st.header("🍲 Neue Speise/Getränk kalkulieren")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name")
            kat = st.selectbox("Kategorie", ["Speise", "Getränk"])
            ek = st.number_input("Warenwert Netto (€)", value=2.50)
        with col2:
            gemeinkosten = st.slider("Gemeinkosten %", 0, 100, 25)
            vk = st.number_input("Verkaufspreis Brutto (€)", value=12.50)
            mwst = st.radio("MwSt", [19, 7], horizontal=True)

        netto_vk = vk / (1 + mwst/100)
        selbstkosten = ek * (1 + gemeinkosten/100)
        gewinn = netto_vk - selbstkosten
        marge = (gewinn / netto_vk * 100) if netto_vk > 0 else 0

        if st.button("Speichern"):
            st.session_state['rezepte'].append({"Name": name, "Kat": kat, "VK": vk, "Marge %": round(marge, 2)})
            st.success(f"{name} gespeichert!")

    # --- 3. PERSONAL & ABSATZ-CHECK ---
    elif page == "📅 Personal & Absatz-Check":
        st.header("📅 Wochenplaner & Absatz-Analyse")
        t1, t2 = st.tabs(["➕ Planung", "📋 Wochenübersicht"])

        with t1:
            col1, col2 = st.columns(2)
            with col1:
                m_tag = st.selectbox("Wochentag", tage)
                m_name = st.text_input("Mitarbeiter")
                m_std = st.number_input("Stunden", value=8.0)
            with col2:
                m_lohn = st.number_input("Lohn/Std", value=15.0)
                umsatz_target = st.number_input("Tagesumsatz-Ziel (€)", value=1000.0)

            if st.button("Schicht speichern"):
                kosten = m_std * m_lohn * 1.2
                st.session_state['schichten'].append({
                    "Tag": m_tag, "Name": m_name, "Kosten": kosten, "Umsatz_Soll": umsatz_target
                })
                st.success("Gespeichert!")

        with t2:
            for tag in tage:
                schichten_tag = [s for s in st.session_state['schichten'] if s['Tag'] == tag]
                with st.expander(f"📌 {tag}", expanded=True):
                    if schichten_tag:
                        t_kosten = sum(s['Kosten'] for s in schichten_tag)
                        t_umsatz = schichten_tag[0]['Umsatz_Soll']
                        
                        st.write(f"**Personalkosten:** {t_kosten:.2f} € | **Ziel:** {t_umsatz:.2f} €")
                        
                        # --- NEU: EINSTELLBARE VERTEILUNG ---
                        st.markdown("---")
                        st.write("⚖️ **Umsatz-Verteilung anpassen**")
                        s_anteil = st.slider(f"Anteil Speisen vs. Getränke ({tag})", 0, 100, 70, key=f"slide_{tag}")
                        g_anteil = 100 - s_anteil
                        st.caption(f"Verteilung: {s_anteil}% Speisen | {g_anteil}% Getränke")

                        if st.session_state['rezepte']:
                            df_rez = pd.DataFrame(st.session_state['rezepte'])
                            avg_speise = df_rez[df_rez['Kat'] == "Speise"]['VK'].mean() if not df_rez[df_rez['Kat'] == "Speise"].empty else 0
                            avg_getraenk = df_rez[df_rez['Kat'] == "Getränk"]['VK'].mean() if not df_rez[df_rez['Kat'] == "Getränk"].empty else 0
                            
                            c1, c2 = st.columns(2)
                            if avg_speise > 0:
                                anz_s = (t_umsatz * (s_anteil/100)) / avg_speise
                                c1.metric("Benötigte Speisen", f"~ {int(anz_s)} Stk.", f"Ø {avg_speise:.2f}€")
                            if avg_getraenk > 0:
                                anz_g = (t_umsatz * (g_anteil/100)) / avg_getraenk
                                c2.metric("Benötigte Getränke", f"~ {int(anz_g)} Stk.", f"Ø {avg_getraenk:.2f}€")
                        else:
                            st.warning("Bitte erst Gerichte kalkulieren!")
                        
                        # Löschen von Schichten
                        for i, s in enumerate(st.session_state['schichten']):
                            if s['Tag'] == tag:
                                if st.button(f"🗑️ {s['Name']}", key=f"del_{tag}_{i}"):
                                    st.session_state['schichten'].pop(i)
                                    st.rerun()
                    else:
                        st.write("Keine Planung für diesen Tag.")

    # --- 4. SPEISEKARTE ---
    elif page == "📜 Meine Speisekarte":
        st.header("📜 Speisekarte")
        if st.session_state['rezepte']:
            df = pd.DataFrame(st.session_state['rezepte'])
            st.dataframe(df, use_container_width=True)
            if st.button("Gesamte Karte leeren"):
                st.session_state['rezepte'] = []
                st.rerun()
        else:
            st.info("Noch keine Daten vorhanden.")
