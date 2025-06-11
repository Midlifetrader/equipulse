import streamlit as st
import yfinance as yf

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

# Portfolio weergeven + verwijderknop
st.subheader("📋 Mijn portfolio")

if st.session_state.portfolio:
    verwijder = st.empty()  # tijdelijke plek voor verwijderen
    for i, aandeel in enumerate(st.session_state.portfolio):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"✅ {aandeel}")
            try:
                stock = yf.Ticker(aandeel)
                data = stock.history(period="1d")
                prijs = data['Close'][0]
                st.write(f"Huidige prijs: ${prijs:.2f}")
            except Exception as e:
                st.write("Koersdata niet beschikbaar.")
        with col2:
            if st.button(f"Verwijder {aandeel}", key=f"verwijder_{i}"):
                st.session_state.portfolio.pop(i)
                st.experimental_rerun()
else:
    st.write("Nog geen aandelen toegevoegd.")
