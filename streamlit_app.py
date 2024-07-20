import streamlit as st
import json
import requests
from streamlit_lightweight_charts import renderLightweightCharts

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def transform_data(data):
    transformed = []
    for entry in data:
        transformed_entry = {
            "open": float(entry["open"]),
            "high": float(entry["high"]),
            "low": float(entry["low"]),
            "close": float(entry["close"]),
            "time": int(entry["open_time"] / 1000)  # Convert milliseconds to seconds
        }
        transformed.append(transformed_entry)
    return transformed

# URL de la API
url = 'http://104.46.208.49:8000/api/klines/binance?ticker=ETHUSDT&timeframe=1m&limit=5'

# Cargar datos
st.write("Cargando datos...")
data = fetch_data(url)
transformed_data = transform_data(data)

# Configurar gráfico
chartOptions = {
    "layout": {
        "textColor": 'black',
        "background": {
            "type": 'solid',
            "color": 'white'
        }
    }
}

seriesCandlestickChart = [{
    "type": 'Candlestick',
    "data": transformed_data,
    "options": {
        "upColor": '#26a69a',
        "downColor": '#ef5350',
        "borderVisible": False,
        "wickUpColor": '#26a69a',
        "wickDownColor": '#ef5350'
    }
}]

st.subheader("Candlestick Chart with Watermark")

renderLightweightCharts([
    {
        "chart": chartOptions,
        "series": seriesCandlestickChart
    }
], 'candlestick')
