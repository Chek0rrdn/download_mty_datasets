import logging
import re
import shutil
import os
import wget

from common import *
import page_object as po

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@tiempo_de_ejecucion
def run():

    cities = list(config()['municipios'].keys())


    for city in cities:
        monterrey = po.tr_Page(city)

        logging.info(f'Empezando el proceso para el municipio de {city}')

        if not os.path.isdir(f'./archivos-{city}/'):
            os.mkdir(f'./archivos-{city}/')
            os.mkdir(f'./archivos-{city}/years/')

        for year in monterrey.years:
            if not os.path.isdir(f'./archivos-{city}/years/{year}/'):
                os.mkdir(f'./archivos-{city}/years/{year}')
                os.mkdir(f'./archivos-{city}/years/{year}/archivos')


        for i,j in zip(monterrey.nom_documentos, monterrey.links_documentos):
            logging.info(f'\nEmpezando a descargar {i}')
            document_year = re.findall(r'\d{4,4}', i)
            document_year = ''.join(document_year)
            wget.download(
                url=j,
                out=f'./archivos-{city}/years/{document_year}/archivos/{i}.xlsx'
            )
        shutil.move(f'./archivos-{city}', '../transform/')
        # shutil.copy(f'./archivos-{city}', '../transform/')


if __name__ == '__main__':
    run()