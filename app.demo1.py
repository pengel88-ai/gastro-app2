import streamlit as st
import pandas as pd

# --- 1. GRUNDKONFIGURATION ---
st.set_page_config(
    page_title="GastroPro 2026",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SICHERHEIT & LOGIN ---
def check_login():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.title("🔐 Gastro 2026 Login")
            password = st.text_input("Bitte Passwort eingeben", type="password")
            if st.button("Anmelden"):
                if password == "Gastro2026":
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Falsches Passwort")
        return False
    return True

# --- 3. DATEN-MANAGEMENT (DEMO) ---
def init_data():
    if "menu" not in st.session_state:
        st.session_state["menu"] = []
    if "staff" not in st.session_state:
        st.session_state["staff"] = []

def load_demo_content():
    # 1. Speisekarte & Getränke (Komplett)
    # Kalkulation: Marge = (NettoVK - EK) / NettoVK * 100
    # Wir speichern hier EK und Brutto VK
    demo_menu = [
        # --- VORSPEISEN (4) ---
        {"Kategorie": "Vorspeise", "Name": "Rinder Carpaccio", "EK": 4.50, "VK": 16.90, "Rezept": "80g Rinderfilet, Parmesan, Rucola, Trüffelöl"},
        {"Kategorie": "Vorspeise", "Name": "Ziegenkäse Taler", "EK": 3.20, "VK": 12.50, "Rezept": "Ziegenkäse, Honig, Thymian, Blattsalat"},
        {"Kategorie": "Vorspeise", "Name": "Vitello Tonnato", "EK": 4.10, "VK": 15.90, "Rezept": "Kalbsfleisch, Thunfischsauce, Kapern"},
        {"Kategorie": "Vorspeise", "Name": "Bruschetta Mix", "EK": 1.80, "VK": 8.90, "Rezept": "Ciabatta, Tomatenwürfel, Knoblauch, Basilikum"},
        # --- HAUPTGÄNGE (5) ---
        {"Kategorie": "Hauptgang", "Name": "Wiener Schnitzel", "EK": 7.50, "VK": 26.90, "Rezept": "180g Kalb, Panade, Bratkartoffeln, Preiselbeeren"},
        {"Kategorie": "Hauptgang", "Name": "Zwiebelrostbraten", "EK": 9.20, "VK": 29.50, "Rezept": "220g Rumpsteak, Röstzwiebeln, Spätzle, Jus"},
        {"Kategorie": "Hauptgang", "Name": "Lachsfilet", "EK": 6.80, "VK": 24.50, "Rezept": "Lachs, Spinat, Risotto"},
        {"Kategorie": "Hauptgang", "Name": "Trüffel Pasta", "EK": 4.50, "VK": 19.50, "Rezept": "Tagliatelle, Sahne, Trüffelpaste, Parmesan"},
        {"Kategorie": "Hauptgang", "Name": "Beyond Burger", "EK": 5.10, "VK": 18.90, "Rezept": "Vegan Patty, Bun, Salat, Pommes"},
        # --- DESSERTS (3) ---
        {"Kategorie": "Dessert", "Name": "Schoko Malheur", "EK": 2.20, "VK": 9.50, "Rezept": "Schokokuchen flüssiger Kern, Vanilleeis"},
        {"Kategorie": "Dessert", "Name": "Kaiserschmarrn", "EK": 1.90, "VK": 10.90, "Rezept": "Teig, Rosinen, Zwetschgenröster"},
        {"Kategorie": "Dessert", "Name": "Panna Cotta", "EK": 1.50, "VK": 8.50, "Rezept": "Sahne, Vanille, Beerenragout"},
        # --- GETRÄNKE (Wein, Bier, AFG, Heiß, Cocktails) ---
        {"Kategorie": "Wein", "Name": "Grauburgunder 0,2l", "EK": 1.80, "VK": 7.50, "Rezept": "Offenausschank"},
        {"Kategorie": "Wein", "Name": "Primitivo 0,2l", "EK": 2.10, "VK": 8.20, "Rezept": "Offenausschank"},
        {"Kategorie": "Bier", "Name": "Helles vom Fass 0,5l", "EK": 1.10, "VK": 4.90, "Rezept": "Fass"},
        {"Kategorie": "Bier", "Name": "Weizenbier 0,5l", "EK": 1.20, "VK": 5.20, "Rezept": "Flasche"},
        {"Kategorie": "AFG", "Name": "Cola / Fanta 0,4l", "EK": 0.90, "VK": 4.50, "Rezept": "Postmix"},
        {"Kategorie": "AFG", "Name": "Tafelwasser 0,7l", "EK": 0.40, "VK": 5.90, "Rezept": "Hausanlage"},
        {"Kategorie": "Heißgetränk", "Name": "Cappuccino", "EK": 0.60, "VK": 3.90, "Rezept": "Siebträger"},
        {"Kategorie": "Heißgetränk", "Name": "Espresso", "EK": 0.30, "VK": 2.90, "Rezept": "Siebträger"},
        {"Kategorie": "Cocktail", "Name": "Aperol Spritz", "EK": 1.90, "VK": 8.50, "Rezept": "Aperol, Prosecco, Soda, Orange"},
        {"Kategorie": "Cocktail", "Name": "Gin Tonic", "EK": 2.50, "VK": 10.50, "Rezept": "4cl Gin, Tonic Water, Gurke"}
    ]
    
    # 2. Mitarbeiter (10 Personen, diverse Positionen)
    # Lohn inkl. ca. 20% Lohnnebenkosten für AG kalkuliert
    demo_staff = [
        {"Name": "Chef Thomas", "Position": "Küche (Leitung)", "Tag": "Mo", "Stunden": 10, "Lohn": 25.00},
        {"Name": "Sous Stefan", "Position": "Küche", "Tag": "Mo", "Stunden": 9, "Lohn": 19.00},
        {"Name": "Jungkoch Ali", "Position": "Küche", "Tag": "Mo", "Stunden": 8, "Lohn": 16.00},
        {"Name": "Spüle Maria", "Position": "Spülküche", "Tag": "Mo", "Stunden": 7, "Lohn": 14.00},
        {"Name": "Oberkellner Jan", "Position": "Service (Leitung)", "Tag": "Mo", "Stunden": 9, "Lohn": 20.00},
        {"Name": "Service Lisa", "Position": "Service", "Tag": "Mo", "Stunden": 8, "Lohn": 15.00},
        {"Name": "Service Tom", "Position": "Service", "Tag": "Mo", "Stunden": 6, "Lohn": 15.00},
        {"Name": "Runner Kevin", "Position": "Service", "Tag": "Mo", "Stunden": 5, "Lohn": 13.50},
        {"Name": "Barchef Mike", "Position": "Bar", "Tag": "Mo", "Stunden": 8, "Lohn": 18.00},
        {"Name": "Barhilfe Sarah", "Position": "Bar", "Tag": "Mo", "Stunden": 6, "Lohn": 14.00}
    ]
    
    st.session_state["menu"] = demo_menu
    st.session_state["staff"] = demo_staff
    st.success("✅ Demo-Daten erfolgreich geladen! (10 MA, volle Karte)")

# --- 4. HAUPTPROGRAMM ---
def main():
    if not check_login():
        return

    init_data()

    # Sidebar
    st.sidebar.title("🍽️ Gastro 2026")
    st.sidebar.markdown("---")
    if st.sidebar.button("✨ Demo-Daten laden"):
        load_demo_content()
        st.rerun()
    
    # Wochenumsatz Ziel Regler in Sidebar
    umsatz_ziel_woche = st.sidebar.number_input("Geplanter Wochenumsatz (€)", value=15000.0, step=500.0)
    
    # Navigation
    tab_dash, tab_kalk, tab_pers = st.tabs(["📊 Dashboard & Analyse", "🍲 Speisekarte & Rezeptur", "📅 Personal & Dienstplan"])

    # ---------------------------------------------------------
    # TAB 1: DASHBOARD & ANALYSE
    # ---------------------------------------------------------
    with tab_dash:
        st.header("📊 Betriebs-Analyse")
        
        # Daten vorbereiten
        df_menu = pd.DataFrame(st.session_state["menu"])
        df_staff = pd.DataFrame(st.session_state["staff"])

        if df_menu.empty or df_staff.empty:
            st.warning("Bitte lade zuerst die Demo-Daten (Sidebar).")
        else:
            # 1. KOSTEN BERECHNUNG
            # Personal: Stunden * Lohn * 1.2 (Lohnnebenkosten Faktor)
            total_personal = (df_staff["Stunden"] * df_staff["Lohn"] * 1.2).sum()
            
            # Wareneinsatz: Wir schätzen den Wareneinsatz basierend auf dem Durchschnitt der Karte
            # Ø Marge der Karte berechnen
            df_menu["NettoVK"] = df_menu["VK"] / 1.19
            df_menu["Wareneinsatz_Quote"] = (df_menu["EK"] / df_menu["NettoVK"])
            avg_wareneinsatz_quote = df_menu["Wareneinsatz_Quote"].mean()
            
            # Theoretischer Wareneinsatz bei Zielumsatz
            total_wareneinsatz = umsatz_ziel_woche * avg_wareneinsatz_quote # vereinfacht Brutto-Basis für Demo
            
            gesamtkosten = total_personal + total_wareneinsatz
            gewinn = umsatz_ziel_woche - gesamtkosten

            # 2. KPI KARTEN
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Personal (Woche)", f"{total_personal:.2f} €", help="Inkl. 20% LNK")
            col2.metric("Ø Wareneinsatz", f"{(avg_wareneinsatz_quote*100):.1f} %")
            col3.metric("Kosten Gesamt", f"{gesamtkosten:.2f} €")
            col4.metric("Potenzieller Gewinn", f"{gewinn:.2f} €", delta_color="normal" if gewinn > 0 else "inverse")

            st.markdown("---")

            # 3. ANALYSE: SIND WIR ZU TEUER / ZU VIEL PERSONAL?
            st.subheader("⚠️ Warn-System")
            c_warn1, c_warn2 = st.columns(2)
            
            # Personalquote Check
            personal_quote = (total_personal / umsatz_ziel_woche * 100) if umsatz_ziel_woche > 0 else 0
            with c_warn1:
                st.write(f"**Personalquote: {personal_quote:.1f}%**")
                if personal_quote > 35:
                    st.error("ACHTUNG: Personalaufwand zu hoch (>35%)! Schichten kürzen oder Umsatz steigern.")
                elif personal_quote < 20:
                    st.success("Personalplanung ist sehr effizient.")
                else:
                    st.info("Personalplanung im grünen Bereich (20-35%).")

            # Kalkulation Check (Gerichte mit schlechter Marge)
            with c_warn2:
                df_menu["Marge_Prozent"] = ((df_menu["NettoVK"] - df_menu["EK"]) / df_menu["NettoVK"] * 100)
                schlechte_marge = df_menu[df_menu["Marge_Prozent"] < 65]
                st.write(f"**Kalkulations-Check:**")
                if not schlechte_marge.empty:
                    st.warning(f"{len(schlechte_marge)} Artikel sind zu günstig kalkuliert (<65% Marge):")
                    st.dataframe(schlechte_marge[["Name", "EK", "VK", "Marge_Prozent"]], hide_index=True)
                else:
                    st.success("Alle Artikel sind profitabel kalkuliert.")

            st.markdown("---")

            # 4. BREAK-EVEN & VERKAUFSZIEL
            st.subheader("🎯 Verkaufsziele")
            st.write(f"Um den Wochenumsatz von **{umsatz_ziel_woche:,.0f}€** zu erreichen:")
            
            # Annahme: Durchschnittsbon Speise vs Getränk
            avg_vk_speise = df_menu[df_menu["Kategorie"].isin(["Hauptgang", "Vorspeise", "Dessert"])]["VK"].mean()
            avg_vk_drink = df_menu[df_menu["Kategorie"].isin(["Wein", "Bier", "AFG", "Cocktail", "Heißgetränk"])]["VK"].mean()
            
            col_target1, col_target2 = st.columns(2)
            
            # Wir nehmen an: 60% Umsatz durch Speisen, 40% durch Getränke
            umsatz_speisen = umsatz_ziel_woche * 0.6
            umsatz_drinks = umsatz_ziel_woche * 0.4
            
            needed_speisen = umsatz_speisen / avg_vk_speise if avg_vk_speise else 0
            needed_drinks = umsatz_drinks / avg_vk_drink if avg_vk_drink else 0
            
            with col_target1:
                st.info(f"🍽️ **{int(needed_speisen)} Speisen** / Woche")
                st.caption(f"ca. {int(needed_speisen/7)} pro Tag (Ø Preis: {avg_vk_speise:.2f}€)")
                
            with col_target2:
                st.info(f"🍹 **{int(needed_drinks)} Getränke** / Woche")
                st.caption(f"ca. {int(needed_drinks/7)} pro Tag (Ø Preis: {avg_vk_drink:.2f}€)")

    # ---------------------------------------------------------
    # TAB 2: SPEISEKARTE & REZEPTUR
    # ---------------------------------------------------------
    with tab_kalk:
        st.header("🍲 Speisekarte & Kalkulation")
        st.info("💡 Du kannst die Werte direkt in der Tabelle bearbeiten (Doppelklick in Zelle).")
        
        # Dateneingabe für neue Gerichte
        with st.expander("➕ Neues Gericht / Getränk anlegen"):
            with st.form("new_dish"):
                c1, c2, c3 = st.columns(3)
                n_kat = c1.selectbox("Kategorie", ["Vorspeise", "Hauptgang", "Dessert", "Wein", "Bier", "AFG", "Cocktail", "Heißgetränk"])
                n_name = c2.text_input("Name")
                n_rez = c3.text_input("Rezeptur (Kurzform)")
                
                c4, c5 = st.columns(2)
                n_ek = c4.number_input("EK Netto (€)", 0.0, 100.0, 2.0)
                n_vk = c5.number_input("VK Brutto (€)", 0.0, 200.0, 10.0)
                
                if st.form_submit_button("Hinzufügen"):
                    st.session_state["menu"].append({
                        "Kategorie": n_kat, "Name": n_name, "EK": n_ek, "VK": n_vk, "Rezept": n_rez
                    })
                    st.rerun()
        
        # EDITABLE DATAFRAME
        if st.session_state["menu"]:
            df_edit_menu = pd.DataFrame(st.session_state["menu"])
            
            # Berechnete Spalten für Anzeige
            df_edit_menu["Marge %"] = (( (df_edit_menu["VK"]/1.19) - df_edit_menu["EK"]) / (df_edit_menu["VK"]/1.19) * 100).round(1)
            
            # Der Editor erlaubt Änderungen
            edited_menu = st.data_editor(
                df_edit_menu,
                num_rows="dynamic",
                column_config={
                    "Marge %": st.column_config.NumberColumn(format="%.1f %%", disabled=True),
                    "VK": st.column_config.NumberColumn(format="%.2f €"),
                    "EK": st.column_config.NumberColumn(format="%.2f €"),
                    "Rezept": st.column_config.TextColumn(width="large")
                },
                hide_index=True,
                key="menu_editor"
            )
            
            # Speichern der Änderungen zurück in Session State (ohne die berechnete Spalte)
            # Hinweis: Streamlit speichert Änderungen im Key, aber wir wollen sauber bleiben
            # Für diese Demo reicht die Anzeige, aber um es "Persistent" während der Sitzung zu machen:
            # (Komplexere Logik nötig für State-Sync bei data_editor, für Demo OK so)

    # ---------------------------------------------------------
    # TAB 3: PERSONAL & DIENSTPLAN
    # ---------------------------------------------------------
    with tab_pers:
        st.header("📅 Dienstplan & Personalkosten")
        st.info("💡 Hier planst du deine 10 Mitarbeiter. Lösche oder bearbeite Zeilen direkt.")
        
        with st.expander("➕ Neue Schicht hinzufügen"):
            with st.form("new_shift"):
                c1, c2, c3 = st.columns(3)
                p_name = c1.text_input("Mitarbeiter Name")
                p_pos = c2.selectbox("Position", ["Küche", "Service", "Bar", "Spülküche", "Management"])
                p_tag = c3.selectbox("Tag", ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"])
                
                c4, c5 = st.columns(2)
                p_std = c4.number_input("Stunden", 0.0, 15.0, 8.0)
                p_lohn = c5.number_input("Stundenlohn (€)", 0.0, 50.0, 15.0)
                
                if st.form_submit_button("Schicht speichern"):
                    st.session_state["staff"].append({
                        "Name": p_name, "Position": p_pos, "Tag": p_tag, "Stunden": p_std, "Lohn": p_lohn
                    })
                    st.rerun()

        if st.session_state["staff"]:
            df_edit_staff = pd.DataFrame(st.session_state["staff"])
            
            # Kosten pro Schicht berechnen (nur Anzeige)
            df_edit_staff["Kosten_Tag"] = (df_edit_staff["Stunden"] * df_edit_staff["Lohn"] * 1.2).round(2)
            
            edited_staff = st.data_editor(
                df_edit_staff,
                num_rows="dynamic",
                column_config={
                    "Kosten_Tag": st.column_config.NumberColumn(format="%.2f €", disabled=True, label="Kosten (inkl. LNK)"),
                    "Lohn": st.column_config.NumberColumn(format="%.2f €"),
                    "Position": st.column_config.SelectboxColumn(options=["Küche", "Service", "Bar", "Spülküche", "Management"])
                },
                hide_index=True,
                key="staff_editor"
            )
            
            # Quick Stats unten drunter
            st.write("---")
            c_sum1, c_sum2 = st.columns(2)
            c_sum1.metric("Geplante Stunden Gesamt", f"{edited_staff['Stunden'].sum():.1f} Std")
            c_sum2.metric("Personalkosten Gesamt", f"{edited_staff['Kosten_Tag'].sum():.2f} €")

if __name__ == "__main__":
    main()
