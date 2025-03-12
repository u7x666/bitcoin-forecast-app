import streamlit as st
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
import mplfinance as mpf
import time

# Function to get the latest Bitcoin data
def get_bitcoin_data():
    url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
    response = requests.get(url)
    data = response.json()
    return data["bpi"]["USD"]["rate_float"]

# Function to generate forecast data
def generate_forecast():
    # You can use a prediction model for real forecasting, for simplicity, using random values
    forecast_1min = get_bitcoin_data() + np.random.uniform(-200, 200)
    forecast_1hr = get_bitcoin_data() + np.random.uniform(-500, 500)
    forecast_4hr = get_bitcoin_data() + np.random.uniform(-1000, 1000)
    
    return forecast_1min, forecast_1hr, forecast_4hr

# Streamlit layout
st.title('Bitcoin Forecast App')

# Create live chart and forecast display
chart_container = st.empty()
forecast_container = st.empty()

# Update every 0.5 seconds
while True:
    forecast_1min, forecast_1hr, forecast_4hr = generate_forecast()

    # Create candlestick chart (using a simple sample data)
    data = {
        "Date": pd.date_range(start="2025-03-13", periods=5, freq='H'),
        "Open": [forecast_1min - 50, forecast_1hr - 150, forecast_4hr - 200, forecast_1min, forecast_1hr],
        "High": [forecast_1min + 50, forecast_1hr + 150, forecast_4hr + 200, forecast_1min + 100, forecast_1hr + 300],
        "Low": [forecast_1min - 100, forecast_1hr - 300, forecast_4hr - 400, forecast_1min - 150, forecast_1hr - 500],
        "Close": [forecast_1min, forecast_1hr, forecast_4hr, forecast_1min + 50, forecast_1hr + 100],
    }
    
    df = pd.DataFrame(data)
    mpf.plot(df, type='candle', style='charles', title="Bitcoin Price Forecast", ylabel='Price (USD)', volume=False)

    chart_container.pyplot(plt)

    forecast_container.write(f"1 Minute Forecast: ${forecast_1min:.2f}")
    forecast_container.write(f"1 Hour Forecast: ${forecast_1hr:.2f}")
    forecast_container.write(f"4 Hours Forecast: ${forecast_4hr:.2f}")
    
    time.sleep(0.5)  # Refresh every 0.5 seconds
