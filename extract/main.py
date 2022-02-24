import logging
import re
import shutil
import pathlib
import wget

import page_object as po
from common import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@tiempo_de_ejecucion
def run():

    cities = list(config()['municipios'].keys())
    CURRENT_DIR = pathlib.Path().resolve()
    TRANSFORM_DIR = CURRENT_DIR.parent.joinpath("transform").resolve()


    for city in cities:

        logging.info(f'Empezando el proceso para el municipio de {city}')
        monterrey = po.tr_Page(city)


        CITY_FILES_PATH = pathlib.Path(CURRENT_DIR.joinpath(f"archivos-{city}"))


        if not CITY_FILES_PATH.exists():
            CITY_FILES_PATH.mkdir()
            CITY_FILES_PATH.joinpath("years").mkdir()


        for year in monterrey.years:
            if not CITY_FILES_PATH.joinpath("years", str(year)).exists():
                CITY_FILES_PATH.joinpath("years", str(year)).mkdir()
                CITY_FILES_PATH.joinpath("years", str(year), "archivos").mkdir()


        for i,j in zip(monterrey.nom_documentos, monterrey.links_documentos):
            logging.info(f'\nEmpezando a descargar {i}')
            document_year = re.findall(r'\d{4,4}', i)
            document_year = ''.join(document_year)
            wget.download(
                url=j,
                out= str(CITY_FILES_PATH.joinpath("years", str(document_year), "archivos")) + str(f'/{i}.xlsx')
            )
        
        logging.info(f'\nSe movieron los archivos de la Ciudad de {city} a la carpeta Transform!!!\n')
        shutil.move(str(CITY_FILES_PATH), str(TRANSFORM_DIR))


if __name__ == '__main__':
    run()
