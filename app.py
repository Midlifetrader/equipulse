import streamlit as st
import yfinance as yf
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(page_title="Aandelen Dashboard", layout="wide")

st.title("📈 Aandelen Dashboard")

# Initialiseer portfolio & keuze
if "portfolio" not in st.session_state:
    st.session_state.portfolio = []
if "geselecteerd" not in st.session_state:
    st.session_state.geselecteerd = None

# Functie om % verandering te berekenen
def get_percentage_change(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="2d")  # 2 dagen data ophalen (vandaag en gisteren)
        if len(data) >= 2:
            close_prices = data['Close']
            pct_change = (close_prices[-1] - close_prices[-2]) / close_prices[-2] * 100
            return pct_change
        else:
            return None
    except:
        return None

# Sidebar - Portfolio en aandelen toevoegen
with st.sidebar:
    st.subheader("📋 Portfolio")
    ticker = st.text_input("Voeg aandeel toe (bijv. AAPL)")
    if st.button("➕ Toevoegen"):
        if ticker:
            ticker = ticker.upper()
            if ticker not in st.session_state.portfolio:
                st.session_state.portfolio.append(ticker)
                st.success(f"{ticker} toegevoegd.")
            else:
                st.warning(f"{ticker} staat al in de lijst.")

    # Portfolio weergeven met % verandering
    for aandeel in st.session_state.portfolio:
        pct_change = get_percentage_change(aandeel)
        kleur = ""
        if pct_change is not None:
            if pct_change > 0:
                kleur = "🟩"
            elif pct_change < 0:
                kleur = "🟥"
            else:
                kleur = ""
        label = f"{aandeel} "
        if pct_change is not None:
            label += f"{kleur} {pct_change:.2f}%"
        else:
            label += " (geen data)"

        if st.button(label):
            st.session_state.geselecteerd = aandeel

    if st.session_state.portfolio:
        if st.button("🗑 Verwijder geselecteerde"):
            if st.session_state.geselecteerd in st.session_state.portfolio:
                st.session_state.portfolio.remove(st.session_state.geselecteerd)
                st.session_state.geselecteerd = None
                st.experimental_rerun()

# Geen aandeel geselecteerd? Kies de eerste
if not st.session_state.geselecteerd and st.session_state.portfolio:
    st.session_state.geselecteerd = st.session_state.portfolio[0]

# Layout: 3 kolommen
col1, col2, col3 = st.columns([1, 2, 1])

# MIDDEN: Koersgrafiek
with col2:
    if st.session_state.geselecteerd:
        aandeel = st.session_state.geselecteerd
        st.subheader(f"📊 Grafiek voor {aandeel}")

        periode_map = {
            "1 dag": "1d", "5 dagen": "5d", "1 maand": "1mo",
            "3 maanden": "3mo", "6 maanden": "6mo",
            "1 jaar": "1y", "5 jaar": "5y", "10 jaar": "10y", "Max": "max"
        }
        keuze = st.selectbox("Kies periode:", list(periode_map.keys()))
        periode = periode_map[keuze]

        try:
            stock = yf.Ticker(aandeel)
            data = stock.history(period=periode)
            if not data.empty:
                st.line_chart(data['Close'])
                st.write(f"Huidige prijs: ${data['Close'][-1]:.2f}")
            else:
                st.warning("Geen data gevonden.")
        except:
            st.error("Fout bij ophalen van koersgegevens.")

# RECHTS: Nieuws + sentiment
with col3:
    st.subheader("📰 Nieuws & Sentiment")

    api_key = "aaba881fc80e4ea8b23113534527b52a" 
    analyzer = SentimentIntensityAnalyzer()

    def haal_nieuws(ticker):
        zoekterm = ticker + " stock"
        url = f"https://newsapi.org/v2/everything?q={zoekterm}&sortBy=publishedAt&apiKey={
