import bs4
import re
import requests
from common import config
from urllib.parse import urljoin


class Page:
    def __init__(self, uuid_municipio) -> None:
        self._config = config()['municipios'][uuid_municipio]
        self._queries = self._config['queries']
        self._url = self._config['url']
        self._html = None

        self._visit(self._url)

    
    def _select(self, query_string):
        return self._html.select(query_string)


    def _visit(self, url):
        cabeceras = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
            'User-Agent': 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16.2',
            'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52',
            'User-Agent': 'Opera/9.80 (X11; Linux x86_64; U; Ubuntu/10.10 (maverick); pl) Presto/2.7.62 Version/11.01',
        }

        respuesta = requests.get(url, headers=cabeceras)
        respuesta.raise_for_status()

        self._html = bs4.BeautifulSoup(respuesta.text, 'html.parser')



class tr_Page(Page):
    def __init__(self, uuid_municipio) -> None:
        super().__init__(uuid_municipio)

        self._pattern = self._config['queries']['patron_regex']
        self._page = self._config['pagina_base']
        
        self.__doc_names = None
        self.__links_docs = None
        self.__years = None

        self.__datos()



    def __datos(self):
        doc_names = []
        well_formed_links = []
        years = set()

        datos = self._select(self._queries['nombre_archivos'])
        
        for i in datos:
            if re.search(self._pattern, urljoin(self._page, i['href'])):
                doc_names.append(i.get_text())
                year = re.findall(r'\d{4,4}', i.get_text())
                year = ''.join(year)
                years.add(year)
                well_formed_links.append(urljoin(self._page, i['href']))
        
        self.__doc_names = doc_names
        self.__links_docs = well_formed_links
        self.__years = years
        
    
    @property
    def nom_documentos(self):
        return self.__doc_names

    @property
    def links_documentos(self):
        return self.__links_docs
    
    @property
    def years(self):
        return self.__years