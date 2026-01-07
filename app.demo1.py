import streamlit as st
import pandas as pd
import altair as alt

# --- 1. KONFIGURATION ---
st.set_page_config(page_title="GastroPro Suite 2026", page_icon="🍽️", layout="wide")

# --- 2. LOGIN SYSTEM ---
def check_login():
    if "authenticated" not in st.session_state: st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.title("🔐 GastroPro 2026")
            st.info("Bitte anmelden, um Zugriff auf Dienstpläne und Kalkulation zu erhalten.")
            pwd = st.text_input("Passwort", type="password")
            if st.button("Login"):
                if pwd == "Gastro2026":
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Falsches Passwort.")
        return False
    return True

# --- 3. DEMO DATEN (10 MA, Volle Karte) ---
def init_data():
    # A) MITARBEITER (10 Personen, verteilt auf die Woche für die Plantafel)
    if "staff" not in st.session_state:
        st.session_state["staff"] = [
            {"Name": "Chef Thomas", "Pos": "Küche", "Tag": "Mo", "Std": 10, "Lohn": 25.0},
            {"Name": "Chef Thomas", "Pos": "Küche", "Tag": "Di", "Std": 10, "Lohn": 25.0},
            {"Name": "Chef Thomas", "Pos": "Küche", "Tag": "Fr", "Std": 11, "Lohn": 25.0},
            {"Name": "Sous Stefan", "Pos": "Küche", "Tag": "Mo", "Std": 9, "Lohn": 19.0},
            {"Name": "Sous Stefan", "Pos": "Küche", "Tag": "Di", "Std": 9, "Lohn": 19.0},
            {"Name": "Sous Stefan", "Pos": "Küche", "Tag": "Sa", "Std": 10, "Lohn": 19.0},
            {"Name": "Jungkoch Ali", "Pos": "Küche", "Tag": "Fr", "Std": 8, "Lohn": 16.0},
            {"Name": "Jungkoch Ali", "Pos": "Küche", "Tag": "Sa", "Std": 9, "Lohn": 16.0},
            {"Name": "Spüle Maria", "Pos": "Spüle", "Tag": "Fr", "Std": 7, "Lohn": 14.0},
            {"Name": "Spüle Maria", "Pos": "Spüle", "Tag": "Sa", "Std": 8, "Lohn": 14.0},
            {"Name": "Leitung Jan", "Pos": "Service", "Tag": "Fr", "Std": 9, "Lohn": 20.0},
            {"Name": "Leitung Jan", "Pos": "Service", "Tag": "Sa", "Std": 10, "Lohn": 20.0},
            {"Name": "Service Lisa", "Pos": "Service", "Tag": "Mo", "Std": 7, "Lohn": 15.0},
            {"Name": "Service Lisa", "Pos": "Service", "Tag": "Fr", "Std": 8, "Lohn": 15.0},
            {"Name": "Service Tom", "Pos": "Service", "Tag": "Sa", "Std": 8, "Lohn": 15.0},
            {"Name": "Runner Kevin", "Pos": "Service", "Tag": "Sa", "Std": 6, "Lohn": 13.5},
            {"Name": "Barchef Mike", "Pos": "Bar", "Tag": "Fr", "Std": 9, "Lohn": 18.0},
            {"Name": "Barchef Mike", "Pos": "Bar", "Tag": "Sa", "Std": 10, "Lohn": 18.0},
            {"Name": "Barhilfe Sarah", "Pos": "Bar", "Tag": "Sa", "Std": 7, "Lohn": 14.0},
            {"Name": "Aushilfe Tim", "Pos": "Spüle", "Tag": "So", "Std": 5, "Lohn": 13.0}
        ]

    # B) SPEISEKARTE (Umfangreich)
    if "menu" not in st.session_state:
        st.session_state["menu"] = [
            # Vorspeisen
            {"Kat": "Vorspeise", "Name": "Rinder Carpaccio", "EK": 4.50, "VK": 16.90, "Rezept": "80g Filet, Parmesan, Rucola"},
            {"Kat": "Vorspeise", "Name": "Ziegenkäse Taler", "EK": 3.20, "VK": 12.50, "Rezept": "Honig, Thymian, Salat"},
            {"Kat": "Vorspeise", "Name": "Bruschetta", "EK": 1.20, "VK": 7.90, "Rezept": "Tomate, Knoblauch, Ciabatta"},
            {"Kat": "Vorspeise", "Name": "Vitello Tonnato", "EK": 4.10, "VK": 15.90, "Rezept": "Kalb, Thunfischsauce"},
            # Hauptgänge
            {"Kat": "Hauptgang", "Name": "Wiener Schnitzel", "EK": 7.50, "VK": 26.90, "Rezept": "Kalb, Panade, Bratkartoffeln"},
            {"Kat": "Hauptgang", "Name": "Zwiebelrostbraten", "EK": 9.20, "VK": 29.50, "Rezept": "Rumpsteak, Spätzle"},
            {"Kat": "Hauptgang", "Name": "Lachsfilet", "EK": 6.80, "VK": 24.50, "Rezept": "Spinat, Risotto"},
            {"Kat": "Hauptgang", "Name": "Beyond Burger", "EK": 5.10, "VK": 18.90, "Rezept": "Vegan Patty, Pommes"},
            {"Kat": "Hauptgang", "Name": "Trüffel Pasta", "EK": 4.50, "VK": 19.50, "Rezept": "Tagliatelle, frischer Trüffel"},
            # Desserts
            {"Kat": "Dessert", "Name": "Schoko Malheur", "EK": 2.20, "VK": 9.50, "Rezept": "Flüssiger Kern, Eis"},
            {"Kat": "Dessert", "Name": "Kaiserschmarrn", "EK": 1.90, "VK": 10.90, "Rezept": "Zwetschgenröster"},
            {"Kat": "Dessert", "Name": "Crème Brûlée", "EK": 1.50, "VK": 8.50, "Rezept": "Vanille, Zucker"},
            # Getränke
            {"Kat": "Wein", "Name": "Grauburgunder 0,2l", "EK": 1.80, "VK": 7.50, "Rezept": "Offen"},
            {"Kat": "Bier", "Name": "Helles Fass 0,5l", "EK": 1.10, "VK": 4.90, "Rezept": "Fass"},
            {"Kat": "AFG", "Name": "Cola 0,4l", "EK": 0.90, "VK": 4.50, "Rezept": "Postmix"},
            {"Kat": "Heißgetränk", "Name": "Cappuccino", "EK": 0.60, "VK": 3.90, "Rezept": "Siebträger"},
            {"Kat": "Cocktail", "Name": "Aperol Spritz", "EK": 1.90, "VK": 8.50, "Rezept": "Prosecco, Soda"}
        ]

# --- 4. HAUPTPROGRAMM ---
def main():
    if not check_login(): return
    init_data()

    # --- SIDEBAR ---
    st.sidebar.title("🍽️ GastroPro Suite")
    st.sidebar.caption("v4.0 Combined Edition")
    st.sidebar.markdown("---")
    
    # Globaler Umsatz-Regler für Dashboard
    target_sales = st.sidebar.number_input("🎯 Wochenziel Umsatz (€)", value=18000.0, step=1000.0)
    
    if st.sidebar.button("🔄 Demo Reset"):
        st.session_state.clear()
        st.rerun()

    # --- NAVIGATION TABS ---
    tab_dash, tab_plan, tab_menu = st.tabs(["📊 Management Dashboard", "📅 Dienstplan (Visuell)", "🍲 Speisekarte & Kalkulation"])

    # ------------------------------------------------------------------
    # TAB 1: DASHBOARD & ANALYSE
    # ------------------------------------------------------------------
    with tab_dash:
        st.header("📊 Wochen-Auswertung & Forecast")
        
        # Daten laden
        df_staff_calc = pd.DataFrame(st.session_state["staff"])
        df_menu_calc = pd.DataFrame(st.session_state["menu"])
        
        if df_staff_calc.empty or df_menu_calc.empty:
            st.warning("Keine Daten. Bitte Demo laden.")
        else:
            # 1. KOSTEN BERECHNUNG
            # Personal: Stunden * Lohn * 1.2 (Lohnnebenkosten)
            personal_kosten_total = (df_staff_calc["Std"] * df_staff_calc["Lohn"] * 1.2).sum()
            
            # Wareneinsatz (Theoretisch): Wir nehmen den Ø Wareneinsatz der Karte und wenden ihn auf den Zielumsatz an
            df_menu_calc["NettoVK"] = df_menu_calc["VK"] / 1.19
            df_menu_calc["WE_Quote"] = df_menu_calc["EK"] / df_menu_calc["NettoVK"]
            avg_we_quote = df_menu_calc["WE_Quote"].mean()
            
            wareneinsatz_total = target_sales * avg_we_quote
            
            # Gesamt & Gewinn
            kosten_gesamt = personal_kosten_total + wareneinsatz_total
            gewinn = target_sales - kosten_gesamt
            
            # 2. KPI ANZEIGE
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Personal (Woche)", f"{personal_kosten_total:,.2f} €", delta="-30% Ziel", delta_color="inverse")
            c2.metric("Ø Wareneinsatz", f"{(avg_we_quote*100):.1f} %")
            c3.metric("Gesamtkosten", f"{kosten_gesamt:,.2f} €")
            c4.metric("Potenzieller Gewinn", f"{gewinn:,.2f} €", delta="Prognose")
            
            st.markdown("---")
            
            # 3. WARN-SYSTEM
            col_warn1, col_warn2 = st.columns(2)
            
            with col_warn1:
                st.subheader("⚠️ Personal-Effizienz")
                personal_quote = (personal_kosten_total / target_sales * 100) if target_sales > 0 else 0
                st.write(f"Aktuelle Personalquote: **{personal_quote:.1f}%**")
                
                # Chart Kosten pro Bereich
                chart_data = df_staff_calc.copy()
                chart_data["Kosten"] = chart_data["Std"] * chart_data["Lohn"] * 1.2
                st.bar_chart(chart_data.groupby("Pos")["Kosten"].sum())

                if personal_quote > 35:
                    st.error("ACHTUNG: Quote über 35%! Du verplanst zu viel Personal für diesen Umsatz.")
                elif personal_quote < 20:
                    st.success("Sehr effiziente Planung (Unter 20%).")
                else:
                    st.info("Planung im optimalen Bereich (20-35%).")

            with col_warn2:
                st.subheader("🎯 Absatz-Ziele")
                st.write(f"Um **{target_sales:,.0f} €** Umsatz zu erreichen, musst du diese Woche verkaufen:")
                
                # Berechnung Absatzmengen
                avg_vk_food = df_menu_calc[df_menu_calc["Kat"].isin(["Vorspeise", "Hauptgang", "Dessert"])]["VK"].mean()
                avg_vk_drink = df_menu_calc[df_menu_calc["Kat"].isin(["Wein", "Bier", "AFG", "Cocktail", "Heißgetränk"])]["VK"].mean()
                
                # Annahme: 60% Food, 40% Drinks Umsatzanteil
                needed_food = (target_sales * 0.6) / avg_vk_food
                needed_drinks = (target_sales * 0.4) / avg_vk_drink
                
                st.info(f"🍽️ **ca. {int(needed_food)} Speisen** (Ø {int(needed_food/7)} pro Tag)")
                st.info(f"🍹 **ca. {int(needed_drinks)} Getränke** (Ø {int(needed_drinks/7)} pro Tag)")
                
                st.caption("Basierend auf den Durchschnittspreisen deiner aktuellen Karte.")

    # ------------------------------------------------------------------
    # TAB 2: DIENSTPLAN (VISUELL)
    # ------------------------------------------------------------------
    with tab_plan:
        st.header("📅 Wochenplaner & Schicht-Management")
        
        # DataFrame aus Session State (für Editor)
        df_plan = pd.DataFrame(st.session_state["staff"])
        
        # --- A) VISUELLE PLANTAFEL ---
        st.markdown("### 👁️ Visuelle Übersicht")
        cols = st.columns(7)
        days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
        colors = {"Küche": "#ffcccc", "Service": "#cce5ff", "Bar": "#e5ccff", "Spüle": "#e0e0e0"} # Pastellfarben für HTML

        for i, day in enumerate(days):
            with cols[i]:
                st.write(f"**{day}**")
                st.markdown("---")
                # Filter für Tag
                day_staff = df_plan[df_plan["Tag"] == day]
                if not day_staff.empty:
                    for _, row in day_staff.iterrows():
                        bg_col = colors.get(row["Pos"], "#f9f9f9")
                        # HTML Card Rendering
                        st.markdown(
                            f"""
                            <div style="background-color:{bg_col}; padding:5px; border-radius:5px; margin-bottom:5px; font-size:0.9em; border:1px solid #ccc;">
                                <b>{row['Name']}</b><br>
                                <span style="color:grey">{row['Pos']}</span> | {row['Std']}h
                            </div>
                            """, unsafe_allow_html=True
                        )
                else:
                    st.caption("-")

        st.markdown("---")
        
        # --- B) EDITOR (VERSCHIEBEN) ---
        st.markdown("### ✏️ Plan bearbeiten & Verschieben")
        st.caption("Nutze die Spalte 'Tag' als Dropdown, um Mitarbeiter zu verschieben. Die Ansicht oben aktualisiert sich sofort.")
        
        # Wir erfassen die Änderungen
        edited_staff_df = st.data_editor(
            df_plan,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Tag": st.column_config.SelectboxColumn("Tag (Verschieben)", options=days, required=True),
                "Pos": st.column_config.SelectboxColumn("Bereich", options=["Küche", "Service", "Bar", "Spüle", "Management"]),
                "Lohn": st.column_config.NumberColumn("€/Std", format="%.2f €"),
                "Std": st.column_config.NumberColumn("Stunden", format="%.1f h")
            },
            hide_index=True,
            key="staff_editor_main"
        )
        
        # Optional: Zusammenfassung unten
        with st.expander("📊 Stunden-Matrix anzeigen"):
             pivot = edited_staff_df.pivot_table(index="Name", columns="Tag", values="Std", aggfunc="sum", fill_value=0)
             pivot = pivot.reindex(columns=days, fill_value=0)
             st.dataframe(pivot, use_container_width=True)

    # ------------------------------------------------------------------
    # TAB 3: SPEISEKARTE & KALKULATION
    # ------------------------------------------------------------------
    with tab_menu:
        st.header("🍲 Speisekarte & Rezepturen")
        
        # Eingabe neues Gericht
        with st.expander("➕ Neues Gericht hinzufügen"):
            with st.form("add_dish"):
                c1, c2, c3 = st.columns(3)
                n_kat = c1.selectbox("Kategorie", ["Vorspeise", "Hauptgang", "Dessert", "Wein", "Bier", "AFG", "Cocktail", "Heißgetränk"])
                n_name = c2.text_input("Name")
                n_rez = c3.text_input("Rezept-Info")
                c4, c5 = st.columns(2)
                n_ek = c4.number_input("EK Netto", 0.0, 100.0, 3.0)
                n_vk = c5.number_input("VK Brutto", 0.0, 200.0, 12.0)
                if st.form_submit_button("Speichern"):
                    st.session_state["menu"].append({"Kat":n_kat, "Name":n_name, "EK":n_ek, "VK":n_vk, "Rezept":n_rez})
                    st.rerun()

        # Editor
        df_menu = pd.DataFrame(st.session_state["menu"])
        
        # Wir zeigen die Marge im Editor an, machen sie aber nicht editierbar (da berechnet)
        # Für die Live-Berechnung im Editor brauchen wir einen Trick oder wir zeigen es in einer zweiten Tabelle
        # Einfacher: Wir nutzen den Editor für EK/VK und zeigen darunter die "bösen" Artikel
        
        edited_menu_df = st.data_editor(
            df_menu,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "VK": st.column_config.NumberColumn(format="%.2f €"),
                "EK": st.column_config.NumberColumn(format="%.2f €"),
                "Kat": st.column_config.SelectboxColumn(options=["Vorspeise", "Hauptgang", "Dessert", "Wein", "Bier", "AFG", "Cocktail", "Heißgetränk"]),
                "Rezept": st.column_config.TextColumn(width="medium")
            },
            hide_index=True,
            key="menu_editor_main"
        )
        
        # Analyse der Eingaben
        if not edited_menu_df.empty:
            edited_menu_df["Netto"] = edited_menu_df["VK"] / 1.19
            edited_menu_df["Marge %"] = ((edited_menu_df["Netto"] - edited_menu_df["EK"]) / edited_menu_df["Netto"] * 100)
            
            st.markdown("### ⚠️ Kalkulations-Check")
            bad_margin = edited_menu_df[edited_menu_df["Marge %"] < 68] # Warnschwelle 68%
            
            if not bad_margin.empty:
                st.error(f"Achtung: {len(bad_margin)} Artikel haben eine kritische Marge (unter 68%):")
                st.dataframe(
                    bad_margin[["Name", "EK", "VK", "Marge %"]].style.format({"Marge %": "{:.1f}%", "EK": "{:.2f}€", "VK": "{:.2f}€"}),
                    use_container_width=True
                )
            else:
                st.success("Top! Alle Artikel sind profitabel kalkuliert.")

if __name__ == "__main__":
    main()
