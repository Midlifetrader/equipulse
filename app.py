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
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.subheader("📰 Laatste nieuws + sentiment")

api_key = "aaba881fc80e4ea8b23113534527b52a"  # 
analyzer = SentimentIntensityAnalyzer()

def haal_nieuws(ticker):
    zoekterm = ticker + " stock"
    url = f"https://newsapi.org/v2/everything?q={zoekterm}&sortBy=publishedAt&apiKey={api_key}&language=nl"
    response = requests.get(url)
    if response.status_code == 200:
        artikelen = response.json()["articles"][:5]  # max 5 artikelen
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
            st.write(f"Sentiment: {label}")
            st.markdown("---")
    else:
        st.error("Kon geen nieuws ophalen.")

# Nieuws ophalen voor elk aandeel
for aandeel in st.session_state.portfolio:
    st.write(f"📢 Nieuws voor: {aandeel}")
    haal_nieuws(aandeel)
