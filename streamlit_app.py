import streamlit as st
import json
import aiohttp
import asyncio
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
            "time": int(entry["open_time"] / 1000)
        }
        transformed.append(transformed_entry)
    return transformed

url = 'http://104.46.208.49:8000/api/klines/binance?ticker=ETHUSDT&timeframe=1m&limit=10'

data = asyncio.run(fetch_data(url))
transformed_data = transform_data(data)

st.write("Original Data:")
st.write(data)

st.write("Transformed Data:")
st.write(transformed_data)

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
        "upColor": COLOR_BULL,
        "downColor": COLOR_BEAR,
        "borderVisible": False,
        "wickUpColor": COLOR_BULL,
        "wickDownColor": COLOR_BEAR
    }
}]

st.subheader("Candlestick Chart with Watermark")

renderLightweightCharts([
    {
        "chart": chartOptions,
        "series": seriesCandlestickChart
    }
], 'candlestick')
