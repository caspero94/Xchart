import streamlit as st
import asyncio
import aiohttp
from streamlit_lightweight_charts import renderLightweightCharts

COLOR_BULL = '#26a69a'
COLOR_BEAR = '#ef5350'

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
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

url = 'http://104.46.208.49:8000/api/klines/binance?ticker=ETHUSDT&timeframe=1m&limit=10'

data = asyncio.run(fetch_data(url))
transformed_data = transform_data(data)

st.write("Datos Transformados:")
st.write(transformed_data)
for entry in transformed_data:
    st.write(f"Types: open={type(entry['open'])}, high={type(entry['high'])}, low={type(entry['low'])}, close={type(entry['close'])}, time={type(entry['time'])}")

datase = [
        { "open": 10, "high": 10.63, "low": 9.49, "close": 9.55, "time": 1642427876 },
        { "open": 9.55, "high": 10.30, "low": 9.42, "close": 9.94, "time": 1642514276 },
        { "open": 9.94, "high": 10.17, "low": 9.92, "close": 9.78, "time": 1642600676 },
        { "open": 9.78, "high": 10.59, "low": 9.18, "close": 9.51, "time": 1642687076 },
        { "open": 9.51, "high": 10.46, "low": 9.10, "close": 10.17, "time": 1642773476 },
        { "open": 10.17, "high": 10.96, "low": 10.16, "close": 10.47, "time": 1642859876 },
        { "open": 10.47, "high": 11.39, "low": 10.40, "close": 10.81, "time": 1642946276 },
        { "open": 10.81, "high": 11.60, "low": 10.30, "close": 10.75, "time": 1643032676 },
        { "open": 10.75, "high": 11.60, "low": 10.49, "close": 10.93, "time": 1643119076 },
        { "open": 10.93, "high": 11.53, "low": 10.76, "close": 10.96, "time": 1643205476 }
    ]
for entry in datase:
    st.write(f"Types: open={type(entry['open'])}, high={type(entry['high'])}, low={type(entry['low'])}, close={type(entry['close'])}, time={type(entry['time'])}")
# Configuración del gráfico
chartOptions = {
    "layout": {
        "textColor": 'black',
        "background": {
            "type": 'solid',
            "color": 'white'
        }
    }
}

# Usar datos estáticos para verificar el gráfico
seriesCandlestickChart = [{
    "type": 'Candlestick',
    "data": transformed_data,  # Intenta primero con datos transformados completos
    "options": {
        "upColor": COLOR_BULL,
        "downColor": COLOR_BEAR,
        "borderVisible": False,
        "wickUpColor": COLOR_BULL,
        "wickDownColor": COLOR_BEAR
    }
}]

st.subheader("Candlestick Chart with Transformed Data")

renderLightweightCharts([
    {
        "chart": chartOptions,
        "series": seriesCandlestickChart
    }
], 'candlestick')
