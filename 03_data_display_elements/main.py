import pandas as pd
import streamlit as st
import yfinance as yf

apple = yf.Ticker("AAPL")
microsoft = yf.Ticker("MSFT")
tickers = ['AAPL', 'MSFT']
# Download data and create DataFrame
df_stocks = yf.download(tickers=tickers,
                        start="2020-01-01",
                        end="2021-01-01")

st.title("Acciones de Apple y Microsoft")

# Los siguientes métodos muestran un dataframe más dinámico
# Show df (method dataframe)
st.dataframe(df_stocks)
# Show df (method write)
st.write(df_stocks)

# Tabla estática
st.table(df_stocks.head(5))

# Métricas
st.metric(label="Etiqueta de la métrica",
          value=900, # valor que se muestra de la métrica
          delta=20, # cambio de la métrica (positivo verde, negativo rojo)
          delta_color="normal") # color de la métrica por default
st.metric(label='Expenses',
          value=900,
          delta=-30,
          delta_color="inverse")