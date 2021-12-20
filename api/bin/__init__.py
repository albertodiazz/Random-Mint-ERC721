from PIL import Image, ImageDraw, ImageFont

if Image.__version__ != '8.4.0':
    raise TypeError('Pillow debe ser la version 8.4.0')

import ipfshttpclient
from ipfshttpclient import client

if ipfshttpclient.__version__ != '0.8.0a2':
    raise TypeError('ipfshttpclient debe ser la version 0.8.0a2')

import numpy as np
import json
import re 
import pandas as pd
from dotenv import dotenv_values,load_dotenv
import requests

#Scrips
from bin import config as c

from bin.creacionImagenes import createImage
from bin.ipfs import uploadPinata
from bin.utils.makeAtributos import makeAtributos
from bin.utils.handlingPendingTransaction import pendingStatus

from bin.utils import getRandomFile
from bin.smartContract import smartContract
