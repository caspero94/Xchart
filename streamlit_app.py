import pandas as pd
import aiohttp
import asyncio
import streamlit as st
from datetime import datetime
from lightweight_charts.widgets import StreamlitChart
# URL de la API
API_URL = 'http://104.46.208.49:8000/api/klines/binance'

# Configuración de Streamlit
st.title("Candlestick Chart from API")

# Obtener datos de la API
async def fetch_data(symbol, timeframe, limit=1000):
    url = f"{API_URL}?ticker={symbol}&timeframe={timeframe}&limit={limit}"
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
            "open_time": int(entry["open_time"]),
            "open": float(entry["open"]),
            "high": float(entry["high"]),
            "low": float(entry["low"]),
            "close": float(entry["close"]),
        }
        transformed.append(transformed_entry)
    return transformed

def get_data(symbol, timeframe):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    data = loop.run_until_complete(fetch_data(symbol, timeframe))
    return data

# Configuración del gráfico
def plot_chart(symbol, timeframe):
    data = get_data(symbol, timeframe)
    if not data:
        st.write(f"No data available for {symbol} with timeframe {timeframe}.")
        return

    # Convertir a DataFrame
    df = pd.DataFrame(data)
    
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df.rename(columns={'open_time': 'date'}, inplace=True)
    df.drop(columns=['close_time', 'base_asset_volume','number_of_trades','taker_buy_volume','taker_buy_base_asset_volume'], inplace=True)
    st.write(df)

    # Mostrar gráfico
    chart = StreamlitChart(width=900, height=600)
    chart.legend(visible=True)
    chart.set(df)
    
    chart.load()

# Interfaz de usuario
symbols = ["BTCUSDT", "ETHUSDT"]  # Ajusta según tus tickers
timeframes = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d"]

selected_symbol = st.selectbox("Select Ticker", symbols)
selected_timeframe = st.selectbox("Select Timeframe", timeframes)

plot_chart(selected_symbol, selected_timeframe)