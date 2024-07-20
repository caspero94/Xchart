import pandas as pd
import asyncio
import aiohttp
import streamlit as st
from lightweight_charts.widgets import StreamlitChart

# Configuración del gráfico
chart = StreamlitChart(width=1200, height=1200)

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                response.raise_for_status()

async def load_data(url):
    data = await fetch_data(url)
    data['open_time'] = await pd.to_datetime(data['open_time'], unit='ms')
    return data

def main():
    st.title("Candlestick Chart from API")

    url = 'http://104.46.208.49:8000/api/klines/binance?ticker=ETHUSDT&timeframe=1m&limit=10'

    # Mostrar un mensaje de carga mientras se obtienen los datos
    st.write("Cargando datos...")

    # Cargar datos de forma asíncrona
    transformed_data = asyncio.run(load_data(url))

    # Convertir los datos a un DataFrame de pandas
    df = pd.DataFrame(transformed_data)

    # Configurar y cargar el gráfico
    chart.set(df)
    chart.load()

if __name__ == "__main__":
    main()
