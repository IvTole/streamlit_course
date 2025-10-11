import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import fetch_california_housing
import streamlit as st
import yfinance as yf

# Data
tickers = ['AAPL', 'MSFT']
df_stocks = yf.download(tickers=tickers,
                        start="2020-01-01",
                        end="2021-01-01")

st.title("Acciones de Apple y Microsoft")

st.dataframe(df_stocks)

st.divider()

st.header("Plots de Apple")
# DataFrame de Apple por nivel
df_apple = df_stocks.xs('AAPL', level=1, axis=1)
df_apple = df_apple.reset_index() # no usar date como index

# Streamlit Line chart
st.line_chart(data=df_apple,
             x="Date",
             y="Close")

# Streamlit Area chart
st.area_chart(data=df_apple,
              x="Date",
              y='Volume')

# Streamilit Bar chart
st.bar_chart(data=df_apple,
             x="Date",
             y=["Open","Close"])

# Streamlit Map (necesito longitude y latitude)
data = fetch_california_housing()
df_cal_haus = pd.DataFrame(data.data, columns=data.feature_names)
df_cal_haus['MedHouseVal'] = data.target

st.map(data=df_cal_haus,
       latitude="Latitude",
       longitude='Longitude')

# Matplotlib

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(df_apple['Date'], df_apple["Close"])
ax.set_title('Close vs Date (AAPL)')
ax.set_xlabel('Date')
ax.set_ylabel('Close[USD]')
st.pyplot(fig)