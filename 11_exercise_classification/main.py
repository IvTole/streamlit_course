import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, roc_auc_score, f1_score

import streamlit as st

from mushroom_dict import mushroom_dict

# Funtions

@st.cache_data
def read_data():
    url = 'https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/refs/heads/master/18_caching_capstone/data/mushrooms.csv'
    df = pd.read_csv(url)
    #df = pd.read_csv("data/mushrooms.csv")
    df = df.drop(columns=['population','bruises','habitat','stalk-root','ring-number','veil-color','veil-type','cap-shape','cap-surface','cap-color','gill-spacing','gill-attachment','stalk-shape'])

    df_original = df.copy()

    # pre processing
    # Class encoding
    le = LabelEncoder()
    df["class"] = le.fit_transform(df["class"])
    # Features encoding
    X_cols = df.drop(columns="class").columns
    oe = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    df[X_cols] = oe.fit_transform(df[X_cols])

    # defaults por columna (la moda de df_original, en códigos originales)
    defaults = {c: df_original[c].mode(dropna=True)[0] for c in X_cols}

    # Feature matrix and target vector
    X = df.drop(columns='class')
    y = df["class"]

    # orden canónico que vio el encoder
    encoder_cols = list(oe.feature_names_in_)  # debería coincidir con list(X_cols)

    return df_original, df, X, y, oe, defaults, encoder_cols

@st.cache_data
def model_evaluation(_model,X_train,X_test,y_train,y_test):
    
    f1_score_list = []
    selected_features_list = []

    for k in range(1,14):
        selector = SelectKBest(mutual_info_classif, k=k)
        selector.fit(X_train, y_train)

        selected_features_mask = selector.get_support()
        selected_features = X_train.columns[selected_features_mask]
        selected_features_list.append(selected_features)
        sel_X_train = selector.transform(X_train)
        sel_X_test = selector.transform(X_test)
    
        _model.fit(sel_X_train,y_train)
        y_pred = _model.predict(sel_X_test)
        f1 = round(f1_score(y_true=y_test,
                            y_pred=y_pred,
                            average="weighted"),3)
        f1_score_list.append(f1)
    
    return f1_score_list, selected_features_list

@st.cache_data
def model_selection(_model,X_train,X_test,y_train,y_test,k):
    
    selector = SelectKBest(mutual_info_classif, k=k)
    selector.fit(X_train, y_train)

    selected_features_mask = selector.get_support()
    selected_features = X_train.columns[selected_features_mask]
    
    sel_X_train = selector.transform(X_train)
    sel_X_test = selector.transform(X_test)
    
    _model.fit(sel_X_train,y_train)
    y_pred = _model.predict(sel_X_test)
    f1 = round(f1_score(y_true=y_test,
                        y_pred=y_pred,
                        average="weighted"),3)
    
    return gbc, f1, selected_features

def f1_comparison_fig(f1_score_list):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    x = np.arange(1,14)
    y = f1_score_list

    ax.bar(x,y,width=0.2)
    ax.set_xlabel("Number of features selected using mutual information")
    ax.set_ylabel("F1-Score (weighted)")
    ax.set_ylim(0,1.2)
    ax.set_xticks(np.arange(1,14))
    ax.set_xticklabels(np.arange(1,14), fontsize=12)

    for i, v in enumerate(y):
        plt.text(x=i+1, y=v+0.05, s=str(v), ha="center", size=7)
    
    plt.close()

    return fig



if __name__ == "__main__":

    # Load Data
    df_original, df_mushrooms, X, y, oe, defaults, encoder_cols = read_data()

    st.title("Mushroom classifier 🍄")

    # DataFrame expander
    with st.expander(label='See full Dataframe here:'):
        st.write(df_mushrooms)

    c1, c2 = st.columns(2)
    # Number of selected features
    with c1:
        k = st.slider(label='Number of selected features',
                    min_value=1,
                    max_value=X.shape[1],
                    value=5,
                    step=1)
        
        X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=0.3,
                                                        shuffle=True,
                                                        stratify=y,
                                                        random_state=42)
        gbc = GradientBoostingClassifier(max_depth=5,
                                     random_state=42)
        gbc, f1, selected_features = model_selection(gbc,
                                            X_train=X_train,
                                            X_test=X_test,
                                            y_train=y_train,
                                            y_test=y_test,
                                            k=k)
    
        st.metric(label='Current f1-score',
                  value=f1)
        
    with c2:
        st.subheader("Current used features")
        for item in selected_features:
            st.write('* '+ item)


    with st.form(key='mushroom_form'):
        st.subheader('Step 1: Select the values for prediction')

        col1, col2, col3 = st.columns(3)

        with col1:
            od = st.selectbox(label='Odor',
                        options=df_original["odor"].map(mushroom_dict["odor"]).unique(),
                        index=1)
            ssar = st.selectbox(label='Stalk surface above ring',
                        options=df_original["stalk-surface-above-ring"].map(mushroom_dict["stalk-surface-above-ring"]).unique(),
                        index=1)
            scbr = st.selectbox(label='Stalk color below ring',
                        options=df_original["stalk-color-below-ring"].map(mushroom_dict["stalk-color-below-ring"]).unique(),
                        index=4)
        with col2:
            gs = st.selectbox(label='Gill size',
                        options=df_original["gill-size"].map(mushroom_dict["gill-size"]).unique(),
                        index=1)
            ssbr = st.selectbox(label='Stalk surface below ring',
                        options=df_original["stalk-surface-below-ring"].map(mushroom_dict["stalk-surface-below-ring"]).unique(),
                        index=1)
            rt = st.selectbox(label='Ring type',
                        options=df_original["ring-type"].map(mushroom_dict["ring-type"]).unique(),
                        index=1)
        with col3:
            gc = st.selectbox(label='Gill color',
                        options=df_original["gill-color"].map(mushroom_dict["gill-color"]).unique(),
                        index=0)
            scar = st.selectbox(label='Stalk color above ring',
                        options=df_original["stalk-color-above-ring"].map(mushroom_dict["stalk-color-above-ring"]).unique(),
                        index=3)
            spc = st.selectbox(label='Spore print color',
                        options=df_original["spore-print-color"].map(mushroom_dict["spore-print-color"]).unique(),
                        index=0)
        st.subheader('Step 2: Ask the model for a prediction')
            
        st.form_submit_button(label='Predict', type='primary')

    cols_dict = {
    "odor":od,
    "gill-size":gs,
    "gill-color":gc,
    "stalk-surface-above-ring":ssar,
    "stalk-surface-below-ring":ssbr,
    "stalk-color-above-ring":scar,
    "stalk-color-below-ring":scbr,
    "ring-type":rt,
    "spore-print-color":spc
    }

    df_test = pd.DataFrame()

    # 1) DataFrame con TODAS las columnas que vio el encoder
    df_pred_full = pd.DataFrame({c: [defaults[c]] for c in encoder_cols})  # inicia con modos
    # Sobrescribe solo las elegidas por el usuario
    for c, v in cols_dict.items():
        if c in df_pred_full.columns:
            df_pred_full[c] = [v[0]] # solo la letra inicial

    # 2) Asegura el orden exacto (por si acaso)
    df_pred_full = df_pred_full[encoder_cols]

    # 3) Transforma con el MISMO encoder (coherencia total)
    X_pred_full_enc = oe.transform(df_pred_full)  # ndarray (1, n_features)

    # 4) Emular SelectKBest: seleccionar solo columnas elegidas
    #    Mapeamos nombres -> posiciones según 'encoder_cols'
    idx_selected = [encoder_cols.index(c) for c in selected_features]
    X_pred_enc_selected = X_pred_full_enc[:, idx_selected]

    st.write("Vector de test (solo features seleccionadas):")
    st.write(X_pred_enc_selected)

    # 5) Predecir con el modelo YA entrenado
    # Predicción del modelo
    pred = gbc.predict(X_pred_enc_selected)[0]

    if pred == 1:
        st.markdown("### ☠️ El hongo es **venenoso**")
    else:
        st.markdown("### 🍽️ El hongo es **comestible**")