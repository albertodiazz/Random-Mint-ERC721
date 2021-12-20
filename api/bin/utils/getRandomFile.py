from bin import c
from bin import pd
import os
import random

def getFiles(path):
    path = path
    list_of_files = []

    for root, dirs, files in os.walk(path):
        for file in files:
            list_of_files.append(file)
    nameFiles = []        
    for name in list_of_files:
        nameFiles.append(str(name).split('.')[0])
    return nameFiles

def getrandomFileMint(minteados,archivoTotales):
    for x in range(len(minteados)):
        archivoTotales.remove(minteados[x])
    randomFile = random.randrange(len(archivoTotales))
    return archivoTotales[randomFile]

def run():
    #El nombre de la imagen siempre debe ser igual al del json minteado
    jsonsMinteados = getFiles(c.PATHMETADATA)
    imagenesCreadas = getFiles(c.PATHIMAGENES)
    r = getrandomFileMint(jsonsMinteados,imagenesCreadas)
    return r
