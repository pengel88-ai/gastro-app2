import streamlit as st
def check_password():
    """Gibt True zurück, wenn das Passwort korrekt ist."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # Login-Maske anzeigen
    password = st.text_input("Bitte Passwort eingeben", type="password")
    if st.button("Anmelden"):
        if password == "DeinGeheimesPasswort123": # Hier dein Passwort festlegen Aw98zHFxknJMSMN
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("Falsches Passwort")
    return False

if not check_password():
    st.stop()  # Zeige den Rest der App nicht an
st.set_page_config(page_title="GastroPro Kalkulator", layout="centered")

st.title("👨‍🍳 GastroPro: Kalkulation & Planung")
st.markdown("---")

# SEITENMENÜ
menu = st.sidebar.selectbox("Menü", ["Dashboard", "Speisen-Kalkulation", "Personal-Planung"])

if menu == "Speisen-Kalkulation":
    st.header("🍲 Neue Speise kalkulieren")
    
    gericht_name = st.text_input("Name des Gerichts", "Wiener Schnitzel")
    
    col1, col2 = st.columns(2)
    with col1:
        wareneinsatz = st.number_input("Wareneinsatz Netto (€)", min_value=0.0, value=4.50, step=0.10)
        ziel_marge = st.slider("Ziel-Marge (%)", 50, 90, 75)
    
    # Kalkulationslogik
    netto_preis = wareneinsatz / (1 - (ziel_marge / 100))
    brutto_preis = netto_preis * 1.19  # 19% MwSt
    
    with col2:
        st.metric("Empf. Verkaufspreis (Brutto)", f"{brutto_preis:.2f} €")
        st.write(f"Deine Marge: {ziel_marge}%")

    if st.button("Gericht Speichern"):
        st.success(f"{gericht_name} wurde zur Karte hinzugefügt!")

elif menu == "Personal-Planung":
    st.header("📅 Personal-Check")
    
    umsatz_erwartet = st.number_input("Erwarteter Tagesumsatz (€)", min_value=0, value=2000)
    st.info("Trage hier ein, wie viele Mitarbeiter heute arbeiten:")
    
    anzahl_service = st.number_input("Anzahl Servicekräfte", 1, 10, 2)
    st.number_input("Anzahl Köche", 1, 10, 2)
    st.number_input("Stunden pro Schicht", 1, 12, 8)
    stundenlohn = st.number_input("Durchschn. Stundenlohn (€)", 12.0, 30.0, 15.0)
    
    # Personalkosten berechnen (vereinfacht: Personal gesamt * Stunden * Lohn)
    personal_kosten = (anzahl_service + 2) * 8 * stundenlohn
    quote = (personal_kosten / umsatz_erwartet) * 100 if umsatz_erwartet > 0 else 0
    
    st.markdown("---")
    st.subheader("Analyse")
    
    if quote > 30:
        st.error(f"Warnung: Personalkostenquote bei {quote:.1f}%! (Ziel: < 30%)")
    else:
        st.success(f"Top! Personalkostenquote liegt bei {quote:.1f}%.")

elif menu == "Dashboard":
    st.header("📊 Tages-Dashboard")
    st.write("Hier fließen alle Daten zusammen.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Umsatz-Forecast", "2.500 €")
    col2.metric("Personal-Kosten", "520 €", "-5%")
    col3.metric("Waren-Einsatz", "32%", "Stabil")
    
    st.bar_chart({"Umsatz": [2100, 2300, 2500, 2200, 2800], "Kosten": [1500, 1600, 1550, 1400, 1700]})
