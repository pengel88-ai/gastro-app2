import streamlit as st
import pandas as pd
import altair as alt

# --- 1. KONFIGURATION ---
st.set_page_config(page_title="GastroPro Suite 2026", page_icon="🍽️", layout="wide")

# --- 2. LOGIN SYSTEM ---
def check_login():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.title("🔐 GastroPro 2026")
            pwd = st.text_input("Passwort", type="password")
            if st.button("Login"):
                if pwd == "Gastro2026":
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Falsches Passwort.")
        return False
    return True

# --- 3. DATEN-INIT (MIT 8-STUNDEN-SCHICHTEN) ---
def init_data():
    if "staff" not in st.session_state:
        # 10 Mitarbeiter gleichmäßig verteilt (jeweils 8 Std)
        st.session_state["staff"] = [
            {"Name": "Chef Thomas", "Pos": "Küche", "Tag": "Mo", "Std": 8, "Lohn": 25.0},
            {"Name": "Chef Thomas", "Pos": "Küche", "Tag": "Di", "Std": 8, "Lohn": 25.0},
            {"Name": "Chef Thomas", "Pos": "Küche", "Tag": "Mi", "Std": 8, "Lohn": 25.0},
            {"Name": "Chef Thomas", "Pos": "Küche", "Tag": "Do", "Std": 8, "Lohn": 25.0},
            {"Name": "Chef Thomas", "Pos": "Küche", "Tag": "Fr", "Std": 8, "Lohn": 25.0},
            {"Name": "Sous Stefan", "Pos": "Küche", "Tag": "Mi", "Std": 8, "Lohn": 19.0},
            {"Name": "Sous Stefan", "Pos": "Küche", "Tag": "Do", "Std": 8, "Lohn": 19.0},
            {"Name": "Sous Stefan", "Pos": "Küche", "Tag": "Fr", "Std": 8, "Lohn": 19.0},
            {"Name": "Sous Stefan", "Pos": "Küche", "Tag": "Sa", "Std": 8, "Lohn": 19.0},
            {"Name": "Sous Stefan", "Pos": "Küche", "Tag": "So", "Std": 8, "Lohn": 19.0},
            {"Name": "Jungkoch Ali", "Pos": "Küche", "Tag": "Mo", "Std": 8, "Lohn": 16.0},
            {"Name": "Jungkoch Ali", "Pos": "Küche", "Tag": "Di", "Std": 8, "Lohn": 16.0},
            {"Name": "Jungkoch Ali", "Pos": "Küche", "Tag": "Fr", "Std": 8, "Lohn": 16.0},
            {"Name": "Jungkoch Ali", "Pos": "Küche", "Tag": "Sa", "Std": 8, "Lohn": 16.0},
            {"Name": "Jungkoch Ali", "Pos": "Küche", "Tag": "So", "Std": 8, "Lohn": 16.0},
            {"Name": "Leitung Jan", "Pos": "Service", "Tag": "Mi", "Std": 8, "Lohn": 20.0},
            {"Name": "Leitung Jan", "Pos": "Service", "Tag": "Do", "Std": 8, "Lohn": 20.0},
            {"Name": "Leitung Jan", "Pos": "Service", "Tag": "Fr", "Std": 8, "Lohn": 20.0},
            {"Name": "Leitung Jan", "Pos": "Service", "Tag": "Sa", "Std": 8, "Lohn": 20.0},
            {"Name": "Leitung Jan", "Pos": "Service", "Tag": "So", "Std": 8, "Lohn": 20.0},
            {"Name": "Service Lisa", "Pos": "Service", "Tag": "Mo", "Std": 8, "Lohn": 15.0},
            {"Name": "Service Lisa", "Pos": "Service", "Tag": "Di", "Std": 8, "Lohn": 15.0},
            {"Name": "Service Lisa", "Pos": "Service", "Tag": "Mi", "Std": 8, "Lohn": 15.0},
            {"Name": "Service Lisa", "Pos": "Service", "Tag": "Sa", "Std": 8, "Lohn": 15.0},
            {"Name": "Service Lisa", "Pos": "Service", "Tag": "So", "Std": 8, "Lohn": 15.0},
            {"Name": "Service Tom", "Pos": "Service", "Tag": "Do", "Std": 8, "Lohn": 15.0},
            {"Name": "Service Tom", "Pos": "Service", "Tag": "Fr", "Std": 8, "Lohn": 15.0},
            {"Name": "Service Tom", "Pos": "Service", "Tag": "Sa", "Std": 8, "Lohn": 15.0},
            {"Name": "Service Tom", "Pos": "Service", "Tag": "So", "Std": 8, "Lohn": 15.0},
            {"Name": "Service Tom", "Pos": "Service", "Tag": "Mo", "Std": 8, "Lohn": 15.0},
            {"Name": "Runner Kevin", "Pos": "Service", "Tag": "Fr", "Std": 8, "Lohn": 13.5},
            {"Name": "Runner Kevin", "Pos": "Service", "Tag": "Sa", "Std": 8, "Lohn": 13.5},
            {"Name": "Runner Kevin", "Pos": "Service", "Tag": "So", "Std": 8, "Lohn": 13.5},
            {"Name": "Barchef Mike", "Pos": "Bar", "Tag": "Di", "Std": 8, "Lohn": 18.0},
            {"Name": "Barchef Mike", "Pos": "Bar", "Tag": "Do", "Std": 8, "Lohn": 18.0},
            {"Name": "Barchef Mike", "Pos": "Bar", "Tag": "Fr", "Std": 8, "Lohn": 18.0},
            {"Name": "Barchef Mike", "Pos": "Bar", "Tag": "Sa", "Std": 8, "Lohn": 18.0},
            {"Name": "Barchef Mike", "Pos": "Bar", "Tag": "So", "Std": 8, "Lohn": 18.0},
            {"Name": "Barhilfe Sarah", "Pos": "Bar", "Tag": "Fr", "Std": 8, "Lohn": 14.0},
            {"Name": "Barhilfe Sarah", "Pos": "Bar", "Tag": "Sa", "Std": 8, "Lohn": 14.0},
            {"Name": "Barhilfe Sarah", "Pos": "Bar", "Tag": "So", "Std": 8, "Lohn": 14.0},
            {"Name": "Spüle Maria", "Pos": "Spüle", "Tag": "Mi", "Std": 8, "Lohn": 14.0},
            {"Name": "Spüle Maria", "Pos": "Spüle", "Tag": "Do", "Std": 8, "Lohn": 14.0},
            {"Name": "Spüle Maria", "Pos": "Spüle", "Tag": "Fr", "Std": 8, "Lohn": 14.0},
            {"Name": "Spüle Maria", "Pos": "Spüle", "Tag": "Sa", "Std": 8, "Lohn": 14.0},
            {"Name": "Spüle Maria", "Pos": "Spüle", "Tag": "So", "Std": 8, "Lohn": 14.0}
        ]

    if "menu" not in st.session_state:
        st.session_state["menu"] = [
            {"Kat": "Vorspeise", "Name": "Rinder Carpaccio", "EK": 4.50, "VK": 16.90, "Rezept": "80g Filet"},
            {"Kat": "Vorspeise", "Name": "Vitello Tonnato", "EK": 4.10, "VK": 15.90, "Rezept": "Kalb, Thunfisch"},
            {"Kat": "Hauptgang", "Name": "Wiener Schnitzel", "EK": 7.50, "VK": 26.90, "Rezept": "Kalb"},
            {"Kat": "Hauptgang", "Name": "Lachsfilet", "EK": 6.80, "VK": 24.50, "Rezept": "Spinat"},
            {"Kat": "Dessert", "Name": "Schoko Malheur", "EK": 2.20, "VK": 9.50, "Rezept": "Eis"},
            {"Kat": "AFG", "Name": "Cola 0,4l", "EK": 0.90, "VK": 4.50, "Rezept": "Postmix"}
        ]

# --- 4. MAIN APP ---
def main():
    if not check_login(): return
    init_data()

    st.sidebar.title("🍽️ GastroPro 2026")
    target_sales = st.sidebar.number_input("🎯 Wochenumsatz-Ziel (€)", value=18000.0)
    if st.sidebar.button("🔄 Reset"):
        st.session_state.clear()
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📅 Dienstplan", "🍲 Speisekarte"])

    with tab1:
        st.header("📊 Wochen-Analyse")
        df_staff = pd.DataFrame(st.session_state["staff"])
        personal_kosten = (df_staff["Std"] * df_staff["Lohn"] * 1.2).sum()
        quote = (personal_kosten / target_sales * 100) if target_sales > 0 else 0
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Personalkosten", f"{personal_kosten:,.2f} €")
        c2.metric("Umsatz-Ziel", f"{target_sales:,.0f} €")
        c3.metric("Quote", f"{quote:.1f} %")

    with tab2:
        st.header("📅 Visuelle Plantafel")
        days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
        cols = st.columns(7)
        df_plan = pd.DataFrame(st.session_state["staff"])
        
        for i, day in enumerate(days):
            with cols[i]:
                st.write(f"**{day}**")
                day_staff = df_plan[df_plan["Tag"] == day]
                for _, row in day_staff.iterrows():
                    st.markdown(f"<div style='background:#f0f2f6; border-radius:5px; padding:5px; margin-bottom:5px; border-left:3px solid red;'><small><b>{row['Name']}</b><br>{row['Pos']}</small></div>", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("Plan bearbeiten / Verschieben")
        st.data_editor(st.session_state["staff"], num_rows="dynamic", key="editor_staff", use_container_width=True)

    with tab3:
        st.header("🍲 Kalkulation")
        st.data_editor(st.session_state["menu"], num_rows="dynamic", key="editor_menu", use_container_width=True)

if __name__ == "__main__":
    main()
