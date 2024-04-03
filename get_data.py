#%%
import pandas as pd
from bs4 import BeautifulSoup
import requests
from io import StringIO
from datetime import datetime

#%%
url_ieeh = 'https://reportesdeis.minsal.cl/ieeh/2024/Reporte/EstadoRegistroEgresoSeremiResumen.aspx'

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
# %%
df_ieeh=extraeTable(url_ieeh)
# %%
new_header = df_ieeh.iloc[0]
df = df_ieeh[1:]
df.columns = new_header 
df['SEREMI de Salud'] = df['SEREMI de Salud'].fillna(method='ffill')
df_metropolitana = df[df['SEREMI de Salud'] == "SEREMI Metropolitana de Santiago"]
df_metropolitana=df_metropolitana[1:]
# %%
df_metropolitana.to_csv("data/iehh_metropolitana.csv")
# %%
