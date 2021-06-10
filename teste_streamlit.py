import streamlit as st
import pandas as pd
import numpy as np

st.title('Roubos de carros em São Paulo - Usando o dataset da Luana')

DATE_COLUMN = 'dataocorrencia'
DATA_URL = ('https://raw.githubusercontent.com/kikosmoura/streamlit/main/roubos_sp.csv')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, sep=';', nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    data['base'] = 'B02512'
    return data

data_load_state = st.text('Carregando os dados...')
data = load_data(10000)
data = data.dropna()

data_load_state.text("Informações de roubos carregadas com sucesso !!!")

if st.checkbox('Mostre a tabela'):
    st.subheader('Tabela')
    st.write(data)

st.subheader('Número de roubos por dia')
hist_values = np.histogram(data[DATE_COLUMN].dt.day, bins=31, range=(0,31))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
day_to_filter = st.slider('Dia', 0, 31, 15)
filtered_data = data[data[DATE_COLUMN].dt.day == day_to_filter]

st.subheader('Todos em roubos em SP no dia %s' % day_to_filter)
st.map(filtered_data)
