import streamlit as st
import yfinance as yf

st.title("📈 Mijn Aandelen Portfolio met Koersdata")

if "portfolio" not in st.session_state:
    st.session_state.portfolio = []

ticker = st.text_input("Voer een aandeel in (bijv. AAPL of TSLA):")

if st.button("Toevoegen"):
    if ticker:
        st.session_state.portfolio.append(ticker.upper())
        st.success(f"Aandeel {ticker.upper()} toegevoegd!")

st.subheader("📋 Mijn portfolio")

if st.session_state.portfolio:
    for aandeel in st.session_state.portfolio:
        st.write(f"✅ {aandeel}")
        try:
            stock = yf.Ticker(aandeel)
            data = stock.history(period="1d")
            prijs = data['Close'][0]
            st.write(f"Huidige prijs: ${prijs:.2f}")
        except Exception as e:
            st.write("Kon koersdata niet ophalen.")
else:
    st.write("Nog geen aandelen toegevoegd.")

