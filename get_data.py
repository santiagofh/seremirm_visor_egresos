#%%
import pandas as pd
from bs4 import BeautifulSoup
import requests
from io import StringIO
from datetime import datetime

#%%
url_ieeh_2024 = 'https://reportesdeis.minsal.cl/ieeh/2024/Reporte/EstadoRegistroEgresoSeremiResumen.aspx'
url_ieeh_2023 = 'https://reportesdeis.minsal.cl/ieeh/2023/Reporte/EstadoRegistroEgresoSeremiResumen.aspx'

# %%
def extraeTable(url):
    response = requests.get(url)
    response = requests.get(url, timeout=360)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find(id='ctl00_CPH_Cuerpo_GridView1')
        string_io_table = StringIO(str(table))
        df = pd.read_html(string_io_table)[0]
        return df
    else:
        print(f'Error al realizar la solicitud: {response.status_code}')
        return None
def ordenarDataFrame(df_ieeh):
    new_header = df_ieeh.iloc[0]
    df = df_ieeh[1:]
    df.columns = new_header 
    df['SEREMI de Salud'] = df['SEREMI de Salud'].fillna(method='ffill')
    df_metropolitana = df[df['SEREMI de Salud'] == "SEREMI Metropolitana de Santiago"]
    df_metropolitana=df_metropolitana[1:]
    return df_metropolitana
# %%
df_ieeh_2024=extraeTable(url_ieeh_2024)
df_ieeh_2023=extraeTable(url_ieeh_2023)
df_ieeh_2024_2=ordenarDataFrame(df_ieeh_2024)
df_ieeh_2023_2=ordenarDataFrame(df_ieeh_2023)
#%%
df_ieeh_2023_2_nan=df_ieeh_2023_2.loc[df_ieeh_2023_2.Total.isna()==True]
ls_codigo_no_aplica=list(df_ieeh_2023_2_nan['Codigo Establecimiento'])
df_ieeh_2024_2['no_aplica_reporte']="aplica"
df_ieeh_2024_2.loc[df_ieeh_2024_2['Codigo Establecimiento'].isin(ls_codigo_no_aplica), 'no_aplica_reporte'] = 'no aplica'
df_ieeh_2023_2['no_aplica_reporte']="aplica"
df_ieeh_2023_2.loc[df_ieeh_2023_2['Codigo Establecimiento'].isin(ls_codigo_no_aplica), 'no_aplica_reporte'] = 'no aplica'
# %%
df_ieeh_2024_2.to_csv("data/iehh_2024_metropolitana.csv")
df_ieeh_2023_2.to_csv("data/iehh_203_metropolitana.csv")
# %%
