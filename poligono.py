import xmltodict
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import zipfile

class Poligono:
    def __init__(self, coordenadas=None, nome='', descricao='', estilo=''):
        self._coordenadas = coordenadas
        self._nome = nome
        self._descricao = descricao
        self._estilo = estilo

    @property
    def coordenadas(self):
        return self._coordenadas

    @coordenadas.setter
    def coordenadas(self, valor):
        if type(valor) is not list:
            raise ValueError('coordenadas deve ser uma list')
        self._coordenadas = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if type(valor) is not str:
            raise ValueError('nome deve ser uma string')
        self._nome = valor

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        if type(valor) is not str:
            raise ValueError('descrição deve ser uma string')
        self._descricao = valor

    @property
    def estilo(self):
        return self._estilo

    @estilo.setter
    def estilo(self, valor):
        if type(valor) is not str:
            raise ValueError('estilo deve ser uma string')
        self._estilo = valor


    @classmethod
    def extrair_poligonos(cls, arq_name):
        """

        :param arq: kml a ser tratado
        :return: lista de objetos
        """
        if '.kmz' in arq_name:
            with zipfile.ZipFile(arq_name, 'r') as f:
                f.extract('doc.kml', 'TEMP')
                arq_name = 'TEMP\doc.kml'
        with open(f'{arq_name}', 'r+') as f:
            arq = f.read()
        arq = arq.replace('<Folder>', '').replace('</Folder>', '')
        arq = arq.replace('<Document>', '').replace('</Document>', '')
        lista = []
        arq = xmltodict.parse(arq)
        j = arq['kml']['Placemark']
        for p in j:
            try:
                coordenadas_texto = p['Polygon']['outerBoundaryIs']['LinearRing']['coordinates']
                coordenadas_float = []
                try:
                    for coordenada in coordenadas_texto.split():
                        coordenada = [float(coordenada.split(',')[1]), float(coordenada.split(',')[0])]
                        coordenadas_float.append(coordenada)
                    try:
                        nome = p['name']
                    except KeyError:
                        nome = ''
                    try:
                        descricao = p['description']
                    except KeyError:
                        descricao = ''
                    try:
                        estilo = p['styleUrl']
                    except KeyError:
                        estilo = ''
                    pt = Poligono()
                    pt.coordenadas = coordenadas_float
                    pt.nome = nome
                    pt.descricao = descricao
                    pt.estilo = estilo
                    lista.append(pt)
                except:pass
            except:
                continue
        return lista

    def esta_dentro(self, coordenada):
        ponto = Point(coordenada)
        poligono = Polygon(self.coordenadas)
        return poligono.contains(ponto)

class PoligonoComposto:
    def __init__(self, coordenadas=[], nome='', descricao='', estilo=''):
        self._coordenadas = coordenadas
        self._nome = nome
        self._descricao = descricao
        self._estilo = estilo

    @property
    def coordenadas(self):
        return self._coordenadas

    @coordenadas.setter
    def coordenadas(self, valor):
        if type(valor) is not list:
            raise ValueError('coordenadas deve ser uma list')
        self._coordenadas = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if type(valor) is not str:
            raise ValueError('nome deve ser uma string')
        self._nome = valor

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        if type(valor) is not str:
            raise ValueError('descrição deve ser uma string')
        self._descricao = valor

    @property
    def estilo(self):
        return self._estilo

    @estilo.setter
    def estilo(self, valor):
        if type(valor) is not str:
            raise ValueError('estilo deve ser uma string')
        self._estilo = valor

    def esta_dentro(self, coordenada):
        ponto = Point(coordenada)
        for p in self.coordenadas:
            poligono = Polygon(p)
            if poligono.contains(ponto):
                return True
        return False
if __name__ == '__main__':
    pass