import logging
import os
import pathlib

import pandas as pd
from openpyxl import load_workbook

from common import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def clean_excel_files(excel_sucio_ruta):

  xls = load_workbook(filename=excel_sucio_ruta)
  sheet_list = xls.sheetnames
  df_ordered = pd.DataFrame()

  for i in range(1, len(sheet_list)):
    df_temporary = pd.read_excel(
        excel_sucio_ruta, 
        sheet_name= sheet_list[i],
        skiprows= 5
    )
    df_temporary['SHEET'] = sheet_list[i]
    df_ordered = df_ordered.append(df_temporary)

  df_ordered = df_ordered.dropna(how='any')

  return df_ordered


def merge_csv_files():
  pass



@tiempo_de_ejecucion
def run():

  cities = list(config()['municipios'].keys())

  for city in cities:
    path_base = pathlib.Path(f'./archivos-{city}/years/')
    years_folders = [año.name for año in path_base.iterdir() if año.is_dir()] 
    
    for year in years_folders:
      year_path = (f'{path_base}/{year}/archivos')

      files_xlsx = os.listdir(year_path)
          
      for i in files_xlsx:
        excel_path = (year_path+'/'+i)

        my_df = clean_excel_files(excel_sucio_ruta= excel_path)
        my_df.to_csv(year_path+'/'+i+'.csv', index=False)
        
        if os.path.isfile(path=excel_path):
          os.remove(path=excel_path)



if __name__ == '__main__':
    run()
