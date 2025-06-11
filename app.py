import streamlit as st

st.title("📈 Mijn Aandelen Portfolio")

# Sla portfolio op in session_state
if "portfolio" not in st.session_state:
    st.session_state.portfolio = []

# Aandeel toevoegen
ticker = st.text_input("Voer een aandeel in (bijv. AAPL of TSLA):")

if st.button("Toevoegen"):
    if ticker:
        st.session_state.portfolio.append(ticker.upper())
        st.success(f"Aandeel {ticker.upper()} toegevoegd!")

# Portfolio weergeven
st.subheader("📋 Mijn portfolio")
if st.session_state.portfolio:
    for aandeel in st.session_state.portfolio:
        st.write(f"✅ {aandeel}")
else:
    st.write("Nog geen aandelen toegevoegd.")
