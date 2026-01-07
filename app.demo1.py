import streamlit as st
import pandas as pd

# --- 1. KONFIGURATION ---
st.set_page_config(page_title="GastroPro v1.9.7 - Professional Edition", page_icon="👨‍🍳", layout="wide")

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

# --- 3. ERWEITERTE DEMO-DATEN ---
def load_demo_data():
    st.session_state['rezepte'] = [
        {"Name": "Burrata auf Tomatencarpaccio", "Kat": "Vorspeise", "VK": 12.50, "Marge %": 72.0, "Rezept": "1x Burrata, 200g Tomaten, Pesto, Pinienkerne"},
        {"Name": "Wiener Schnitzel vom Kalb", "Kat": "Hauptgang", "VK": 26.90, "Marge %": 65.0, "Rezept": "250g Kalbsrücken, Mehl, Ei, Brösel, 200g Kartoffeln"},
        {"Name": "Mousse au Chocolat", "Kat": "Dessert", "VK": 8.50, "Marge %": 78.0, "Rezept": "Zartbitterschokolade, Sahne, Ei, Zucker"},
        {"Name": "Chardonnay Trocken 0,2l", "Kat": "Wein", "VK": 7.20, "Marge %": 82.0, "Rezept": "Flasche offen"},
        {"Name": "Pils 0,5l", "Kat": "Bier", "VK": 4.90, "Marge %": 85.0, "Rezept": "Fassware"},
        {"Name": "Rhabarberschorle 0,4l", "Kat": "AFG", "VK": 4.50, "Marge %": 88.0, "Rezept": "Direktsaft, Sprudel"},
        {"Name": "Old Fashioned", "Kat": "Cocktails", "VK": 11.50, "Marge %": 84.0, "Rezept": "6cl Bourbon, Zucker, Angostura, Orangenabrieb"},
        {"Name": "Cappuccino", "Kat": "Heißgetränke", "VK": 3.80, "Marge %": 91.0, "Rezept": "Espressobohnen, Vollmilch"}
    ]
    st.success("Erweiterte Gastro-Struktur geladen!")

if check_password():
    if 'rezepte' not in st.session_state: st.session_state['rezepte'] = []
    if 'schichten' not in st.session_state: st.session_state['schichten'] = []

    # Kategorien Definition
    kat_speisen = ["Vorspeise", "Hauptgang", "Dessert"]
    kat_getraenke = ["Wein", "Bier", "AFG", "Cocktails", "Heißgetränke"]
    alle_kategorien = kat_speisen + kat_getraenke

    st.sidebar.title("👨‍🍳 GastroPro v1.9.7")
    if st.sidebar.button("✨ Demo-Daten laden"):
        load_demo_data()
        st.rerun()
    
    page = st.sidebar.radio("Navigation", ["📊 Dashboard", "🍲 Rezeptur & Kalkulation", "📅 Personal & Absatz", "📜 Speisekarte"])

    # --- DASHBOARD ---
    if page == "📊 Dashboard":
        st.header("📊 Dashboard")
        total_umsatz = pd.DataFrame(st.session_state['schichten']).drop_duplicates(subset=['Tag'])['Umsatz_Soll'].sum() if st.session_state['schichten'] else 0
        c1, c2, c3 = st.columns(3)
        c1.metric("Ziel-Umsatz Woche", f"{total_umsatz:.2f} €")
        c2.metric("Anzahl Artikel", len(st.session_state['rezepte']))
        
        if st.session_state['rezepte']:
            df_r = pd.DataFrame(st.session_state['rezepte'])
            avg_marge = df_r['Marge %'].mean()
            c3.metric("Ø Marge", f"{avg_marge:.1f} %")

    # --- REZEPTUR & KALKULATION ---
    elif page == "🍲 Rezeptur & Kalkulation":
        st.header("🍲 Neue Rezeptur anlegen")
        with st.form("kalk_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Name des Artikels")
                kat = st.selectbox("Kategorie", alle_kategorien)
                rezeptur = st.text_area("Rezeptur / Zutatenliste", placeholder="z.B. 200g Fleisch, 10g Salz...")
            with c2:
                ek = st.number_input("EK Netto gesamt (€)", min_value=0.0, value=2.50)
                vk = st.number_input("VK Brutto (€)", min_value=0.0, value=12.00)
                mwst = st.selectbox("MwSt Satz", [19, 7])
            
            if st.form_submit_button("Rezeptur speichern"):
                netto_vk = vk / (1 + mwst/100)
                marge = ((netto_vk - ek) / netto_vk * 100) if netto_vk > 0 else 0
                st.session_state['rezepte'].append({
                    "Name": name, "Kat": kat, "VK": vk, "Marge %": round(marge, 1), "Rezept": rezeptur
                })
                st.success(f"Artikel '{name}' wurde der Speisekarte hinzugefügt!")

    # --- PERSONAL & ABSATZ ---
    elif page == "📅 Personal & Absatz":
        st.header("📅 Wochenplanung")
        # (Logik wie zuvor, nutzt die neuen Durchschnittspreise der Kategorien)
        st.info("Hier kannst du Schichten planen und den Absatz-Mix berechnen.")
        # ... (Schicht-Eingabe Code hier einfügen wie in v1.9.6)

    # --- SPEISEKARTE (GLIEDERUNG) ---
    elif page == "📜 Speisekarte":
        st.header("📜 Strukturierte Speisekarte")
        
        if not st.session_state['rezepte']:
            st.info("Noch keine Rezepte vorhanden. Nutze die Demo-Daten oder die Kalkulation.")
        else:
            # Unterteilung in Speisen und Getränke
            st.subheader("🍴 Speisen")
            for sub_kat in kat_speisen:
                items = [r for r in st.session_state['rezepte'] if r['Kat'] == sub_kat]
                if items:
                    with st.expander(f"{sub_kat} ({len(items)})"):
                        for i, it in enumerate(items):
                            col_a, col_b = st.columns([3, 1])
                            col_a.write(f"**{it['Name']}**")
                            col_a.caption(f"Rezeptur: {it['Rezept']}")
                            col_b.write(f"{it['VK']:.2f} €")
            
            st.markdown("---")
            st.subheader("🍷 Getränke")
            for sub_kat in kat_getraenke:
                items = [r for r in st.session_state['rezepte'] if r['Kat'] == sub_kat]
                if items:
                    with st.expander(f"{sub_kat} ({len(items)})"):
                        for i, it in enumerate(items):
                            col_a, col_b = st.columns([3, 1])
                            col_a.write(f"**{it['Name']}**")
                            col_a.caption(f"Info: {it['Rezept']}")
                            col_b.write(f"{it['VK']:.2f} €")
