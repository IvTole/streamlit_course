import streamlit as st
import pandas as pd
import yfinance as yf

# Data
tickers = ['AAPL', 'MSFT']
df_stocks = yf.download(tickers=tickers,
                        start="2020-01-01",
                        end="2021-01-01")
df_apple = df_stocks.xs('AAPL', level=1, axis=1)
df_apple = df_apple.reset_index() # no usar date como index


st.title("Streamlit layout")

# Sidebar
with st.sidebar:
    st.write("Esto es un sidebar")

# Columnas
col1, col2, col3 = st.columns(3) # Se especifica el número de columnas

col1.write("Texto en columna 1")
slider = col2.slider("Escoge un valor",
                     min_value=0,
                     max_value=10,
                     value=5)
col3.write(slider)

st.divider()

# Tabs
tab1, tab2 = st.tabs(['Line plot', 'Bar plot']) # se especifica el titulo de cada tab

with tab1:
    tab1.write("Un gráfico de línea")
    st.line_chart(data=df_apple,
                  x = 'Date',
                  y=["Close", "Open"])
with tab2:
    tab2.write("Un gráfico de barras")
    st.bar_chart(data=df_apple,
                 x="Date",
                 y="Volume")

# Expander (elemento colapsable)
with st.expander("Click to expand"):
    st.write("Este texto solo se ve cuando se expande este elemento")

# Container
with st.container():
    st.write("Esto está adentro del contenedor")
st.write("Esto está afuera del contenedor")
