import sys
import os
import random
from bin import Image, ImageFont, ImageDraw
from bin import np
from bin import json
from bin import c

class LimiteCreacionImagenes(Exception):
    pass
#Hay que cambiar el codigo para que solo genere una cada que se presione el boton de random
def createImage(width,height,pixel):
    #img = Image.fromarray(pixeles)
    centro = 0
    size = 0
    if pixel > 9:
        centro = 1
        size = 2
    else:  
        centro = 0
        size = 1
    myFont = ImageFont.truetype('FreeMono.ttf', int(width/size))
    name = 'numero'+ str(pixel) + '.jpg'

    img = Image.new( mode = "RGB", size = (width, height))
    d = ImageDraw.Draw(img)
    d.text((width/5, (height/5)*centro), str(pixel), font=myFont, fill=(255, 255, 255))
    img.save(c.PATHIMAGENES+name)
    return name

def ImagenesExistentes():
    listNumbers = []
    if len(os.listdir(c.PATHIMAGENES)) != 0:
        for img in os.listdir(c.PATHIMAGENES):
            for m in img.split('.jpg'):
                digit = m.split('numero')[-1]
                if digit.isdigit():
                    listNumbers.append(int(digit))
                    ordenandoNumberos = sorted(listNumbers)
        if len(os.listdir(c.PATHIMAGENES)) != c.RANDOMSERIE + 1:
            loop = True
            lastNumber = None
            while(loop):
                r = random.randint(0,c.RANDOMSERIE)
                if r not in ordenandoNumberos:
                    lastNumber = r
                    #print('Stop el loop')
                    loop=False
            return int(lastNumber)
        else:
            raise LimiteCreacionImagenes({'status':'se alcanzo el limite de la serie Random'})
    else:
        print('Aun no se ha creado ninguna imagen')
        return random.randint(0,c.RANDOMSERIE)


def run():
    pixelRandom = ImagenesExistentes()
    name = createImage(400,400,pixelRandom)
    return name.split('.jpg')[0]

