import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Aandelen Tracker", layout="centered")

st.title("📈 Mijn Aandelen Portfolio")

# Initialiseer portfolio in session state
if "portfolio" not in st.session_state:
    st.session_state.portfolio = []

# Aandeel toevoegen
ticker = st.text_input("Voer een aandeel in (bijv. AAPL of TSLA):")

if st.button("Toevoegen"):
    if ticker:
        ticker = ticker.upper()
        if ticker not in st.session_state.portfolio:
            st.session_state.portfolio.append(ticker)
            st.success(f"Aandeel {ticker} toegevoegd!")
        else:
            st.warning(f"{ticker} zit al in je portfolio.")

# Portfolio weergeven
st.subheader("📋 Mijn portfolio")

if st.session_state.portfolio:
    for i, aandeel in enumerate(st.session_state.portfolio):
        st.markdown(f"### ✅ {aandeel}")

        col1, col2 = st.columns([4, 1])

        with col1:
            # Tijdselectie
            periode_map = {
                "1 dag": "1d",
                "5 dagen": "5d",
                "1 maand": "1mo",
                "3 maanden": "3mo",
                "6 maanden": "6mo",
                "1 jaar": "1y",
                "5 jaar": "5y",
                "10 jaar": "10y",
                "Maximaal": "max"
            }
            keuze = st.selectbox(
                f"Kies tijdsperiode voor {aandeel}:", 
                list(periode_map.keys()), 
                key=f"periode_{aandeel}"
            )
            periode = periode_map[keuze]

            # Data ophalen en tonen
            try:
                stock = yf.Ticker(aandeel)
                data = stock.history(period=periode)

                if not data.empty:
                    huidige_prijs = data['Close'][-1]
                    st.write(f"Huidige prijs: ${huidige_prijs:.2f}")
                    st.line_chart(data['Close'])
                else:
                    st.write("⚠️ Geen data beschikbaar voor deze periode.")
            except Exception as e:
                st.write("❌ Koersdata kon niet worden opgehaald.")

        with col2:
            # Verwijderknop
            if st.button(f"🗑 Verwijder", key=f"verwijder_{i}"):
                st.session_state.portfolio.pop(i)
                st.experimental_rerun()
else:
    st.write("Nog geen aandelen toegevoegd.")
