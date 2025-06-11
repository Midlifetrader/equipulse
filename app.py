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

# Aandeel toevoegen
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

    # Portfolio weergeven
    for aandeel in st.session_state.portfolio:
        if st.button(aandeel):
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

# ✅ MIDDEN: Koersgrafiek
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

# 📰 RECHTS: Nieuws + sentiment
with col3:
    st.subheader("📰 Nieuws & Sentiment")

    api_key = "aaba881fc80e4ea8b23113534527b52a"  
    analyzer = SentimentIntensityAnalyzer()

    def haal_nieuws(ticker):
        zoekterm = ticker + " stock"
        url = f"https://newsapi.org/v2/everything?q={zoekterm}&sortBy=publishedAt&apiKey={api_key}&language=nl"
        response = requests.get(url)
        if response.status_code == 200:
            artikelen = response.json()["articles"][:5]
            for artikel in artikelen:
                titel = artikel["title"]
                url = artikel["url"]
                sentiment = analyzer.polarity_scores(titel)["compound"]
                if sentiment >= 0.05:
                    label = "😊 Positief"
                elif sentiment <= -0.05:
                    label = "😠 Negatief"
                else:
                    label = "😐 Neutraal"

                st.markdown(f"**[{titel}]({url})**")
                st.caption(f"Sentiment: {label}")
                st.markdown("---")
        else:
            st.warning("Nieuws kon niet worden opgehaald.")

    if st.session_state.geselecteerd:
        haal_nieuws(st.session_state.geselecteerd)
