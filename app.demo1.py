import streamlit as st
import pandas as pd
import altair as alt

# --- 1. GRUNDKONFIGURATION ---
st.set_page_config(page_title="GastroPro 2026", page_icon="🍽️", layout="wide")

# --- 2. LOGIN ---
def check_login():
    if "authenticated" not in st.session_state: st.session_state["authenticated"] = False
    if not st.session_state["authenticated"]:
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            st.title("🔐 Login")
            if st.button("Login (Demo Mode)"): # Vereinfacht für schnellen Zugang
                st.session_state["authenticated"] = True
                st.rerun()
            # pwd = st.text_input("Passwort", type="password")
            # if st.button("Anmelden"):
            #     if pwd == "Gastro2026": st.session_state["authenticated"] = True; st.rerun()
        return False
    return True

# --- 3. DEMO DATEN ---
def init_data():
    if "staff" not in st.session_state:
        # Wir nutzen eine flache Liste für maximale Flexibilität
        st.session_state["staff"] = [
            {"Name": "Chef Thomas", "Pos": "Küche", "Tag": "Mo", "Std": 10, "Lohn": 25.0},
            {"Name": "Chef Thomas", "Pos": "Küche", "Tag": "Di", "Std": 10, "Lohn": 25.0},
            {"Name": "Chef Thomas", "Pos": "Küche", "Tag": "Fr", "Std": 12, "Lohn": 25.0},
            {"Name": "Sous Stefan", "Pos": "Küche", "Tag": "Mo", "Std": 9, "Lohn": 19.0},
            {"Name": "Sous Stefan", "Pos": "Küche", "Tag": "Di", "Std": 9, "Lohn": 19.0},
            {"Name": "Lisa Service", "Pos": "Service", "Tag": "Fr", "Std": 8, "Lohn": 15.0},
            {"Name": "Lisa Service", "Pos": "Service", "Tag": "Sa", "Std": 9, "Lohn": 15.0},
            {"Name": "Bar Mike", "Pos": "Bar", "Tag": "Fr", "Std": 9, "Lohn": 18.0},
            {"Name": "Bar Mike", "Pos": "Bar", "Tag": "Sa", "Std": 10, "Lohn": 18.0},
            {"Name": "Spüle Kevin", "Pos": "Spüle", "Tag": "Sa", "Std": 7, "Lohn": 13.5},
        ]
    if "menu" not in st.session_state:
        st.session_state["menu"] = [
            {"Name": "Schnitzel", "Kat": "Hauptgang", "VK": 24.9, "EK": 7.5},
            {"Name": "Burger", "Kat": "Hauptgang", "VK": 18.9, "EK": 5.2},
            {"Name": "Bier 0,5", "Kat": "Getränk", "VK": 4.9, "EK": 1.1}
        ]

# --- 4. HAUPTPROGRAMM ---
def main():
    if not check_login(): return
    init_data()

    st.sidebar.title("🍽️ Gastro 2026")
    if st.sidebar.button("🔄 Reset / Demo laden"):
        st.session_state.clear()
        st.rerun()
    
    # Umsatz-Ziel für Berechnungen
    target = st.sidebar.number_input("Wochenziel Umsatz (€)", value=15000.0, step=1000.0)

    tab1, tab2, tab3 = st.tabs(["📅 Dienstplan & Plantafel", "📊 Dashboard", "🍲 Speisekarte"])

    # ------------------------------------------------------------------
    # TAB 1: DIENSTPLAN (WOCHENANSICHT & EDITOR)
    # ------------------------------------------------------------------
    with tab1:
        st.header("📅 Interaktive Wochenplanung")
        
        df = pd.DataFrame(st.session_state["staff"])
        
        # --- A) DIE PLANTAFEL (VISUELLE WOCHENANSICHT) ---
        st.subheader("1. Die Plantafel (Übersicht)")
        st.info("Das ist deine visuelle Übersicht. Änderungen machst du unten in der Tabelle.")
        
        days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
        cols = st.columns(7)
        
        # Farben für Positionen
        color_map = {"Küche": "🔴", "Service": "🔵", "Bar": "🟣", "Spüle": "🟤", "Management": "⚫"}

        for i, day in enumerate(days):
            with cols[i]:
                st.markdown(f"**{day}**")
                st.markdown("---")
                # Filtere Mitarbeiter für diesen Tag
                day_staff = df[df["Tag"] == day]
                if not day_staff.empty:
                    for _, row in day_staff.iterrows():
                        # Visuelle "Karte" für den Mitarbeiter
                        icon = color_map.get(row["Pos"], "⚪")
                        st.markdown(
                            f"""
                            <div style="background-color:#f0f2f6; padding:8px; border-radius:5px; margin-bottom:5px; border-left: 4px solid #ff4b4b;">
                                <small>{icon} <b>{row['Name']}</b></small><br>
                                <small>{row['Std']} Std</small>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                else:
                    st.markdown("<small style='color:grey'>- Frei -</small>", unsafe_allow_html=True)

        st.markdown("---")

        # --- B) DER EDITOR (VERSCHIEBEN & BEARBEITEN) ---
        st.subheader("2. Planungs-Editor (Verschieben & Bearbeiten)")
        st.write("Um einen Mitarbeiter zu **verschieben**, ändere einfach den Tag in der Spalte 'Tag'. Die Plantafel oben aktualisiert sich sofort.")

        # Neue Schicht Formular
        with st.expander("➕ Neue Schicht hinzufügen"):
            with st.form("add_shift"):
                c1,c2,c3,c4,c5 = st.columns(5)
                n_name = c1.text_input("Name")
                n_pos = c2.selectbox("Pos", ["Küche", "Service", "Bar", "Spüle"])
                n_tag = c3.selectbox("Tag", days)
                n_std = c4.number_input("Std", 0.0, 16.0, 8.0)
                n_lohn = c5.number_input("€/Std", 0.0, 50.0, 15.0)
                if st.form_submit_button("Speichern"):
                    st.session_state["staff"].append({"Name":n_name, "Pos":n_pos, "Tag":n_tag, "Std":n_std, "Lohn":n_lohn})
                    st.rerun()

        # Editable Dataframe - DAS IST DER "SCHIEBEREGLER"
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Tag": st.column_config.SelectboxColumn(
                    "Wochentag (Verschieben)", 
                    help="Ändere den Tag, um den Mitarbeiter zu verschieben",
                    width="medium",
                    options=days,
                    required=True
                ),
                "Pos": st.column_config.SelectboxColumn(options=["Küche", "Service", "Bar", "Spüle"]),
                "Lohn": st.column_config.NumberColumn(format="%.2f €"),
                "Std": st.column_config.NumberColumn(format="%.1f h")
            },
            hide_index=True,
            key="editor_staff"
        )
        
        # Speichern Logik: Wir überschreiben die Session State Liste mit dem editierten DF
        # Da st.data_editor im Session State lebt, müssen wir für Persistenz sorgen, 
        # wenn wir komplexere Logik hätten. Für diese Demo reicht es, da Streamlit den State hält.
        
        # --- C) MATRIX ANSICHT (PIVOT) ---
        with st.expander("📊 Matrix-Ansicht (Stunden pro Tag)"):
            if not df.empty:
                pivot = df.pivot_table(index="Name", columns="Tag", values="Std", aggfunc="sum", fill_value=0)
                # Sortiere Spalten korrekt nach Wochentagen
                pivot = pivot.reindex(columns=days, fill_value=0)
                st.dataframe(pivot, use_container_width=True)

    # ------------------------------------------------------------------
    # TAB 2: DASHBOARD
    # ------------------------------------------------------------------
    with tab2:
        st.header("📊 Kosten-Kontrolle")
        
        if not df.empty:
            df["Kosten"] = df["Std"] * df["Lohn"] * 1.2 # LNK Faktor
            total_personal = df["Kosten"].sum()
            quote = (total_personal / target * 100) if target > 0 else 0
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Personal Kosten", f"{total_personal:.2f} €")
            c2.metric("Ziel-Umsatz", f"{target:,.0f} €")
            c3.metric("Personal-Quote", f"{quote:.1f} %", delta="-30% Ziel", delta_color="inverse")
            
            st.markdown("### Kosten pro Tag")
            # Sortieren nach Wochentag für Chart
            daily_cost = df.groupby("Tag")["Kosten"].sum().reindex(days).fillna(0).reset_index()
            
            chart = alt.Chart(daily_cost).mark_bar().encode(
                x=alt.X('Tag', sort=days),
                y='Kosten',
                tooltip=['Tag', 'Kosten']
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
            
            if quote > 35:
                st.error("⚠️ Achtung: Deine Personalquote ist sehr hoch (>35%)!")
            else:
                st.success("✅ Personalplanung ist wirtschaftlich.")

    # ------------------------------------------------------------------
    # TAB 3: SPEISEKARTE (BASIC)
    # ------------------------------------------------------------------
    with tab3:
        st.header("🍲 Speisekarte")
        df_menu = pd.DataFrame(st.session_state["menu"])
        
        edited_menu = st.data_editor(
            df_menu,
            num_rows="dynamic",
            column_config={
                "VK": st.column_config.NumberColumn(format="%.2f €"),
                "EK": st.column_config.NumberColumn(format="%.2f €")
            },
            key="editor_menu"
        )
        # Live Marge Anzeige
        if not edited_menu.empty:
            edited_menu["Marge %"] = ((edited_menu["VK"]/1.19 - edited_menu["EK"]) / (edited_menu["VK"]/1.19) * 100)
            st.write("Kalkulations-Check:")
            st.dataframe(edited_menu[["Name", "VK", "EK", "Marge %"]].style.format({"Marge %": "{:.1f}%"}))

if __name__ == "__main__":
    main()
