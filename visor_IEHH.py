#%%
import pandas as pd
from bs4 import BeautifulSoup
import requests
from io import StringIO
from datetime import datetime
import streamlit as st
import plotly.express as px

#%%
df_metropolitana=pd.read_csv("data/iehh_metropolitana.csv")
# %%
now = datetime.now()
current_year = now.year
current_month = now.month
# %%
month_columns = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
months_to_check = month_columns[:current_month-2]
condition = pd.concat([df_metropolitana[month].isna() for month in months_to_check], axis=1).any(axis=1)
establecimientos_pendientes = df_metropolitana[condition]
df_metropolitana['Estado'] = 'Al día'
df_metropolitana.loc[establecimientos_pendientes.index, 'Estado'] = 'Pendiente'
estado_counts = df_metropolitana['Estado'].value_counts().reset_index()
estado_counts.columns = ['Estado', 'Número de Establecimientos']
# %%

# Iniciamos Streamlit app
st.title('Estado de Reporte de Egresos Hospitalarios de la SEREMI Metropolitana de Santiago')

# Cambiar a gráfico de torta
fig_pie = px.pie(estado_counts, names='Estado', values='Número de Establecimientos', title='Proporción de Establecimientos al día vs Pendientes')
st.plotly_chart(fig_pie)

# Agregar tablas
st.subheader('Establecimientos Al Día')
st.dataframe(df_metropolitana[df_metropolitana['Estado'] == 'Al día'])

st.subheader('Establecimientos Pendientes')
st.dataframe(df_metropolitana[df_metropolitana['Estado'] == 'Pendiente'])

pendientes_por_mes = df_metropolitana[months_to_check].isna().sum()
pendientes_por_mes = pendientes_por_mes[pendientes_por_mes > 0]  # Opcional: Filtrar meses sin pendientes
pendientes_por_mes_df = pendientes_por_mes.to_frame(name='Número de Pendientes').reset_index()
pendientes_por_mes_df.rename(columns={'index': 'Mes'}, inplace=True)
fig_bar = px.bar(pendientes_por_mes_df, x='Mes', y='Número de Pendientes', title='Número de Pendientes por Mes')
st.plotly_chart(fig_bar)


# %%
