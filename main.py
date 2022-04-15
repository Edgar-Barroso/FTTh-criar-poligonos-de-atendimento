import os
import shutil
import sys

sys.path.insert(0, 'H:\Meu Drive\Python\Dev_FTTh\Objetos_Globais')
from caminho import Caminho
from poligono import Poligono
from geopy.distance import distance
import math
import simplekml

listaP=[]

caminhos = Caminho.extrair_caminhos(rf'Caminho_Clientes.kmz')
for n1, caminho in enumerate(caminhos):
    largura = float(caminho.nome)
    for n2, coordenada in enumerate(caminho.coordenadas):
        if n2 != 0 and (n2%2) != 0:
            coord1 = caminho.coordenadas[n2 - 1]
            coord2 = coordenada
            lat1 = float(coord1[0])
            lat2 = float(coord2[0])
            long1 = float(coord1[1])
            long2 = float(coord2[1])
            hipotenusa = distance((lat1, long1), (lat2, long2)).meters
            catetoad = distance((lat1, long2), (lat1, long1)).meters
            catetoop = math.sqrt((hipotenusa ** 2) - (catetoad ** 2))
            ang = catetoop / hipotenusa
            mov_lat = 0
            mov_long = 0
            tang = catetoop / catetoad
            mov_lat = math.sqrt((largura ** 2) / (tang + 1))
            mov_long = math.sqrt((largura ** 2) - (mov_lat ** 2))
            y = mov_lat * 0.000008997
            x = mov_long * 0.000008997
            if long1 <= long2:
                if lat1 <= lat2:  # caindo pra direito/primeiro ponto baixo
                    a1 = (lat1 + y, long1 - x)
                    a2 = (lat1 - y, long1 + x)
                    b2 = (lat2 - y, long2 + x)
                    b1 = (lat2 + y, long2 - x)
                else:  # caindo pra esquerda/primeiro cima
                    a1 = (lat1 + y, long1 + x)
                    a2 = (lat1 - y, long1 - x)
                    b2 = (lat2 - y, long2 - x)
                    b1 = (lat2 + y, long2 + x)
            else:
                if lat1 <= lat2:  # caindo pra esquerda/primeiro ponto baixo
                    b2 = (lat1 + y, long1 + x)
                    b1 = (lat1 - y, long1 - x)
                    a1 = (lat2 - y, long2 - x)
                    a2 = (lat2 + y, long2 + x)
                else:  # caindo pra direito/primeiro ponto cima
                    b2 = (lat1 + y, long1 - x)
                    b1 = (lat1 - y, long1 + x)
                    a1 = (lat2 - y, long2 + x)
                    a2 = (lat2 + y, long2 - x)
            poligono = Poligono()
            poligono.coordenadas = [[a1[1],a1[0]], [b1[1],b1[0]],[b2[1],b2[0]],[a2[1],a2[0]],[a1[1],a1[0]]]
            listaP.append(poligono)
kmz = simplekml.Kml()
kml = kmz.newfolder(name='')
for poli in listaP:
    poli_simple = kml.newpolygon(outerboundaryis=poli.coordenadas)
    poli_simple.style.polystyle.color = '8835FE25'
kmz.save(rf'poligonos.kmz')
try:
    shutil.rmtree(f'{os.getcwd()}\TEMP')
except FileNotFoundError:
    pass
