import pandas as pd
import aiohttp
import asyncio
import streamlit as st
from datetime import datetime
import pytz
from lightweight_charts.widgets import StreamlitChart
import time

# URL de la API
API_URL = 'http://data-api.japaneast.cloudapp.azure.com:8000/api/klines/'

# Configuración de Streamlit
st.set_page_config(layout="wide")

timezones = [
    'UTC',
    'America/New_York',  # EST/EDT
    'America/Chicago',   # CST/CDT
    'America/Denver',    # MST/MDT
    'America/Los_Angeles',  # PST/PDT
    'Europe/London',     # GMT/BST
    'Europe/Paris',      # CET/CEST
    'Europe/Berlin',     # CET/CEST
    'Europe/Madrid',     # CET/CEST
    'Asia/Tokyo',        # JST
    'Asia/Kolkata',      # IST
    'Asia/Shanghai',     # CST
    'Australia/Sydney',  # AEDT/AEST
]


# Obtener datos de la API
async def fetch_data(exchange, symbol, timeframe, limit=1000):
    url = f"{API_URL}{exchange}?ticker={symbol}&timeframe={timeframe}&limit={limit}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                response.raise_for_status()

def get_data(exchange, symbol, timeframe):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    data = loop.run_until_complete(fetch_data(exchange, symbol, timeframe))
    return data

# Configuración del gráfico
def plot_chart(exchange, symbol, timeframe, timezone):
    data = get_data(exchange, symbol, timeframe)
    if not data:
        st.write(f"No data available for {symbol} with timeframe {timeframe}.")
        return

    # Convertir a DataFrame
    df = pd.DataFrame(data)
    
    df['open_time'] = pd.to_datetime(df['open_time'], unit="ms")
    df = df.iloc[::-1].reset_index(drop=True)
    df.set_index('open_time', inplace=True)

    # Convertir la fecha a la zona horaria seleccionada
    df.index = df.index.tz_localize('UTC').tz_convert(timezone)
    
    # Ajustar a UTC para el gráfico
    df.index = df.index.tz_localize(None)  # Remover la zona horaria para el gráfico

    # Mostrar gráfico
    chart = StreamlitChart(height=400)
    chart.legend(visible=True)
    chart.volume_config(scale_margin_top=0.96)
    chart.time_scale(right_offset=10)
    
    chart.set(df)
    chart.load()

# Interfaz de usuario
col_exchange, col_symbol, col_timeframe, col_candle, col_indicators, col_timezone = st.columns([1, 1, 5, 1, 1, 1], vertical_alignment="bottom")

exchange = ["Binance"]
symbols = ["BTCUSDT", "ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT","DOGEUSDT","ADAUSDT","AVAXUSDT","TRXUSDT","SHIBUSDT", "DOTUSDT", "LINKUSDT", "BCHUSDT", "NEARUSDT", "LTCUSDT", "MATICUSDT", "PEPEUSDT","UNIUSDT","ICPUSDT","ETCUSDT","APTUSDT","FETUSDT","XLMUSDT"]
timeframes = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w"]
type_candle = ["Velas","Línea"]
indicators = ["MACD","MA","MEDIA MOVIL"]
#timezones = pytz.common_timezones  # Lista de todas las zonas horarias


with col_exchange:
    selected_exchange = st.selectbox("Select Exchange", exchange, label_visibility="collapsed")

with col_symbol:
    selected_symbol = st.selectbox("Select Ticker", symbols, label_visibility="collapsed")

with col_timeframe:
    selected_timeframe = st.radio("Select Timeframe", timeframes, index=timeframes.index("1m"),horizontal=True, label_visibility="collapsed")

with col_candle:
    selected_candle = st.selectbox("Select Candle", type_candle, label_visibility="collapsed")

with col_indicators:
    selected_indicators = st.selectbox("Select Indicators", indicators, label_visibility="collapsed")

with col_timezone:
    selected_timezone = st.selectbox("Select Timezone", timezones, label_visibility="collapsed")

while True:
    plot_chart(selected_exchange.lower(), selected_symbol, selected_timeframe, selected_timezone)
    time.sleep(30)  # Espera de 30 segundos antes de volver a ejecutar
    st.rerun()  # Vuelve a ejecutar el script para refrescar el gráfico
