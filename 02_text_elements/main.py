import streamlit as st

## Titulo de la aplicacion
st.title("Título de la aplicación")

## Headers
st.header("Header principal")

## Subheader
st.subheader("Subheader")

## Markdown
st.markdown("Esto es **codigo markdown**")
st.markdown("Estoy escribiendo esto en _markdown_")
st.markdown("# Header1")
st.markdown("## Header2")
st.markdown("### Header3")

## Captions
st.caption("Esto es un caption, nos puede servir para citar cosas.")

## Code blocks
st.code("""
import pandas as pd
pd.read_csv(filename)
""")

## Texto con formato
st.text("Esto es un texto")

## LaTex (math, está medio raro)
st.latex(r'''
\bar{x} = \frac{1}{n} \sum_{i=1}^n x_i; \quad \sigma^2 = \frac{1}{n} \sum_{i=1}^n (x_i - \bar{x})^2                  
''')

## Divider
st.text("Encima del divider")
st.divider()
st.text("Debajo del divider")

# Write (dataframes, images)
st.write('Un texto normal')
