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

st.title('Widgets sobre dataset AAPL')
## Botones
primary_btn = st.button(label="Primary", type="primary")
secondary_btn = st.button(label="Secondary", type="secondary")
## Los botones regresan valores boolean
if primary_btn:
    st.write('Hello from primary')
if secondary_btn:
    st.write('Hello from secondary')

## Checkbox
st.divider()
checkbox = st.checkbox("Remember me")
if checkbox:
    st.write("I will remember you")
else:
    st.write('I will forget you')

## Radio Button
st.divider()

radio = st.radio("Escoge una columna",
                 options=df_apple.columns[1:],
                 index=0, # valor por defecto 
                 horizontal=True)
# Esto regresa el str de la etiqueta
st.line_chart(data=df_apple,
             x="Date",
             y=radio)

## Selectbox
st.divider()
select = st.selectbox("Choose a column",
                      options = df_apple.columns[1:],
                      index=0)
st.line_chart(data=df_apple,
             x="Date",
             y=select)

## Multiselect
st.divider()
multiselect = st.multiselect('Choose as many columns as you want',
                             options = df_apple.columns[1:],
                             default='Close',
                             max_selections=3 # max numero de valores a escoger
                             )
## Esto me regresa una lista con tuplas
## Vamos a usar esto para definir unas métricas
for val in multiselect:
    val_first = df_apple[val].iloc[0]
    val_last = df_apple[val].iloc[-1]
    increase_percentage = round((val_last / val_first) - 1.0,2)
    st.metric(label=val,
              value=str(round(val_last,2))+" USD",
              delta=str(increase_percentage*100) + "%",
              delta_color='normal')
    
## Slider
st.divider()
slider = st.slider('Pick a number',
                   min_value=0,
                   max_value=10,
                   value=5,
                   step=1)
# Me regresa el valor elegido
st.write(slider)

## Text input
st.divider()
text_input = st.text_input("What's your name?",
                           placeholder="Ivan Toledano")
# Me regresa un string
st.write(f'Your name is {text_input}')

## Number input
number_input = st.number_input("Pick a number",
                               min_value=0,
                               max_value=10,
                               value=0,
                               step=1)
st.write(f'You picked number {number_input}')

## Text area
## Como text input pero para textos mas largos
text_area = st.text_area('What do you want to tell me?',
                         height=200, # pixeles del altura del area de escrito
                         placeholder="Write your message here")
# Regresa el string dentro del area
st.write(text_area)