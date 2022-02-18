from asyncio.log import logger
import logging
import os
import wget

from common import *
import page_object as po

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@tiempo_de_ejecucion
def run():

    municipios = list(config()['municipios'].keys())


    for ciudad in municipios:
        test = po.tr_Page(ciudad)

        logging.info(f'Empezando el proceso para el municipio de {ciudad}')

        if not os.path.isdir(f'./archivos-{ciudad}/'):
            os.mkdir(f'./archivos-{ciudad}/')


        for i,j in zip(test.nom_documentos, test.link_documentos):
            logging.info(f'\nEmpezando a descargar {i}')
            wget.download(url=j, out=f'./archivos-{ciudad}/{i}.xlsx')
        


if __name__ == '__main__':
    run()