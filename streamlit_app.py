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
            "open": int(float(entry["open"])),  # Convertir a int
            "high": float(entry["high"]),
            "low": float(entry["low"]),
            "close": float(entry["close"]),
            "time": int(entry["open_time"] / 1000)
        }
        transformed.append(transformed_entry)
    return transformed

# Función asíncrona para cargar datos y renderizar el gráfico
async def load_and_render_chart(url):
    data = await fetch_data(url)
    transformed_data = transform_data(data)
    return transformed_data

# URL de la API
url = 'http://104.46.208.49:8000/api/klines/binance?ticker=ETHUSDT&timeframe=1m&limit=10'

# Cargar datos y mostrar el gráfico
def main():
    st.title("Candlestick Chart")

    # Mostrar un mensaje de carga mientras se obtienen los datos
    st.write("Cargando datos...")

    # Ejecutar la función asíncrona
    transformed_data = asyncio.run(load_and_render_chart(url))

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

    st.subheader("Candlestick Chart with Transformed Data")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesCandlestickChart
        }
    ], 'candlestick')

if __name__ == "__main__":
    main()
