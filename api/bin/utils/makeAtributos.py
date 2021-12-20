from json import load
from bin import json
from bin import c

def makeAtributos(uriHash='Undefined',name='None',descripcion='None'):
    atributos = {
        "name": name,
        "image": uriHash,
        "description": descripcion,
        "attributes": [
            {
                "trait_type": "Shape",
                "value": "Circle"
            },
            {
                "trait_type": "Mood",
                "value": "Sad"
            }
        ],
    }
    atributosJSON = json.dumps(atributos, indent=4)
    atributosJSON = json.loads(atributosJSON)
    with open(c.PATHMETADATA +name+'.json', 'w') as f:
        json.dump(atributosJSON,f)

    return True