import pandas as pd
import streamlit as st
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd

# Streamlit ejecuta el codigo python cada vez que un
# widget cambia
# Queremos ahora que corra hasta que se haga un submit

# Ejercicio de eleccion de menu y reservacion

st.title('Reservación')

with st.form(key='menu_form'):
    st.write('Elige tus opciones del menú')

    appetizer_options = [None, 'Ensalada', 'Sopa', 'Tostadas']
    appetizer_sb = st.selectbox("Entrada",
                                options=appetizer_options,
                                index=0)
    
    main_options = [None, 'Filete de Res', 'Salmón', 'Risotto']
    main_sb = st.selectbox("Plato fuerte",
                           options=main_options,
                           index=0)
    
    dessert_options = [None, 'Tiramisú', 'Pastel', 'Panacota']
    dessert_sb = st.selectbox("Postre",
                              options=dessert_options,
                              index=0)
    
    checkbox = st.checkbox('Traigo mi propio vino')

    date_min = dt.date.today()
    date_max = dt.date.today() + relativedelta(months=2)
    date_input = st.date_input(label='Fecha de la reservación',
                               value='today',
                               min_value=date_min,
                               max_value=date_max)
    
    time_options = pd.date_range(start="08:00", end="18:00", freq="30min")
    hours_str = time_options.strftime("%H:%M").tolist()
    time_input = st.selectbox('Hora de la reservación',
                              options=hours_str,
                              index=0)
    
    allergies = st.text_area('¿Alguna alergia?',
                             placeholder="Déjanos una nota con tus alergias",
                             height=20)

    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    st.markdown('''
### Resumen de la reservación:
''')
    st.write(f'Entrada: {appetizer_sb}')
    st.write(f'Plato fuerte: {main_sb}')
    st.write(f'Postre: {dessert_sb}')
    st.write(f'Traigo mi propio vino: {"yes" if checkbox else "no"}')
    st.write(f'Fecha de la reservación: {date_input}')
    st.write(f'Hora de la reservación: {time_input}')
    st.write(f'Alergias: {allergies}')
