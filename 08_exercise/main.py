import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Data
url = "https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/refs/heads/master/12_dashboard_capstone/data/quarterly_canada_population.csv"
df_ca_pop = pd.read_csv(url)
# Se agrega columna temporal
df_ca_pop["Period"] = df_ca_pop["Quarter"].str.replace(r"Q(\d) (\d{4})", r"\2Q\1", regex=True)
df_ca_pop["Period"] = pd.PeriodIndex(df_ca_pop["Period"], freq="q")
df_ca_pop["Period"] = df_ca_pop["Period"].dt.start_time

st.title("Population of Canada")
st.markdown('''
Source table can be found [here](https://github.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/blob/master/12_dashboard_capstone/data/quarterly_canada_population.csv)
''')

# Expander with dataframe
with st.expander("See full data table"):
    st.dataframe(df_ca_pop)

with st.form(key='pop_form'):
    col1, col2, col3 = st.columns(3)
    col1.write("Choose a starting date")
    q_start = col1.selectbox("Quarter",
                options = ["Q1", "Q2", "Q3"],
                index=2)
    y_start = col1.slider(label='Year',
                min_value=1991,
                max_value=2023,
                step=1,
                value=1991)
    col2.write('Choose an end date')
    q_end = col2.selectbox("Quarter",
                options = ["Q1", "Q2", "Q3"],
                index=1)
    y_end = col2.slider(label='Year',
                min_value=1991,
                max_value=2023,
                step=1,
                value=1992)
    col3.write("Choose a location")
    loc = col3.selectbox(label='Choose a location',
                   options=df_ca_pop.drop(columns=["Quarter","Period"]).columns,
                   index=0)
    
    st.form_submit_button(label='Analyze', type='primary')

# Tabs
tab1, tab2 = st.tabs(['Population change', 'Compare']) # se especifica el titulo de cada tab

# Time start, end, in different formats
d_start = str(q_start) + " " + str(y_start)
ts_start = str(y_start) + str(q_start)
ts_start = pd.Period(ts_start, freq="Q")
ts_start = ts_start.start_time
   

d_end = str(q_end) + " " + str(y_end)
ts_end = str(y_end) + str(q_end)
ts_end = pd.Period(ts_end, freq="Q")
ts_end = ts_end.start_time

try:
    val_start = df_ca_pop[df_ca_pop["Quarter"] == d_start][loc].iloc[0]
    val_end = df_ca_pop[df_ca_pop["Quarter"] == d_end][loc].iloc[0]
except IndexError:
    st.error("No data available. Check your quarter and year selection")
    st.stop() # Detiene el script de streamlit
except Exception as e:
    st.exception(e)

if ts_start > ts_end:
    st.error("Dates don't work. Start date must come before end date")
    st.stop()
# Aquí capturas el IndexError típico que ocurre cuando .iloc[0] falla 
# porque el filtro devolvió 0 filas.

# se calcula el porcentaje de aumento o decremento
prop_inc = round(((val_end/val_start) - 1.0)*100,2)

with tab1:

    tab1.subheader(f'Population change from {d_start} to {d_end}')

    mask = (df_ca_pop["Period"] >= ts_start) & (df_ca_pop["Period"] <= ts_end)
    df_ca_pop_filtered = df_ca_pop[mask]
    
    tab1_col1, tab1_col2 = st.columns(2)
    tab1_col1.metric(label=d_start,
                value=val_start)
    tab1_col1.metric(label=d_end,
                value=val_end,
                delta=str(prop_inc) + "%",
                delta_color='normal')
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(df_ca_pop_filtered["Period"],
            df_ca_pop_filtered[loc])
    ax.set_xlabel("Time")
    ax.set_ylabel("Population")
    ax.set_title(f"Population of {loc}")
    plt.close()
    tab1_col2.pyplot(fig)
    
with tab2:
    tab2.subheader(f'Compare with other locations')
    loc_compare = tab2.multiselect(label='Choose other locations',
                                   options=df_ca_pop.drop(columns=["Quarter","Period"]).columns,
                                   default="Canada")
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for location in loc_compare:
        ax.plot(df_ca_pop_filtered["Period"],
                df_ca_pop_filtered[location],
                label=location)
    ax.set_xlabel("Time")
    ax.set_ylabel("Population")
    ax.set_title(f"Population")
    ax.legend(loc="best")
    plt.close()
    tab2.pyplot(fig)
    