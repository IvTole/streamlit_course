import numpy as np
import pandas as pd
import time
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import streamlit as st

# st.cache_data
# Para tener en el cache resultados
# Dataframes, cálculos de funciones, querys de API
# Básicamente cualquier cosa que regrese un objeto serializable(str, int, float, df, array, list, etc.)

# st.cache_resource
# Recursos que deberían estar disponibles globalmente sobre los usuarios, sesiones y reruns
# Normalmente está limitado a ML y conecciones a bases de datos

st.title("Caching demonstration")

st.button('Test cache')

st.subheader("st.cache_data")

# Se guarda en cache el resultado
@st.cache_data
def cache_this_function():
    time.sleep(2) # 2 seconds
    out = "I'm done running"
    return out

out = cache_this_function()
st.write(out)

st.subheader("st.cache_resource")

# Get data
url = 'https://raw.githubusercontent.com/IvTole/MachineLearning_InferenciaBayesiana_CUGDL/refs/heads/main/data/mtcars/mtcars.csv'
df_mtcars = pd.read_csv(url)

# Linear Regression
X = df_mtcars[['hp', 'disp']]
y = df_mtcars['mpg']
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.2,
                                                    random_state=42)
@st.cache_resource # ya que regresa un modelo
def create_simple_linear_regression(X,y):
    time.sleep(2)
    
    model = LinearRegression()
    model.fit(X,y)

    return model

lr = create_simple_linear_regression(X_train, y_train)
y_pred = lr.predict(X_test)
r2 = r2_score(y_pred=y_pred, y_true=y_test)
st.write(f"The model has a r2 score of {round(r2,2)}")
