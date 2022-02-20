import logging
import os
import openpyxl
import pathlib
import pandas as pd

from common import config
from nltk.corpus import stopwords
#   si es la primera vez ejecutando este programa, descomente y ejecute la siguiente 
#   linea, una vez ejecutada, se puede volver a comentar:
#   nltk.download('stopwords')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def limpia_archivos_excel(excel_sucio_ruta):
  xls = openpyxl.load_workbook(filename=excel_sucio_ruta)
  lista_de_hojas = xls.sheetnames
  df_limpio = pd.DataFrame()

  for i in range(1, len(lista_de_hojas)):
    df_provisional = pd.read_excel(
        excel_sucio_ruta, 
        sheet_name=lista_de_hojas[i],
        skiprows=5
    )
    df_provisional['SHEET'] = lista_de_hojas[i]
    df_limpio = df_limpio.append(df_provisional, ignore_index=True)


  df_limpio = df_limpio.dropna(how='any')

  return df_limpio


def run():

  cities = list(config()['municipios'].keys())

  path_base = pathlib.Path('./archivos-monterrey/years/')
  years_folders = [año.name for año in path_base.iterdir() if año.is_dir()] 
    
  for year in years_folders:
    year_path = (f'{path_base}/{year}/archivos')

    files_xlsx = os.listdir(year_path)
        
    for i in files_xlsx:
      excel_path = (year_path+'/'+i)

      my_df = limpia_archivos_excel(
        excel_sucio_ruta= excel_path
      )
      my_df.to_csv(year_path+'/'+i+'.csv')

      # print(excel_path)
      # print(year_path+'/'+i+'.csv')



if __name__ == '__main__':
    run()
