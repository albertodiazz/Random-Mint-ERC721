from bin import c
from bin import dotenv_values,load_dotenv
from bin import requests,json

config = dotenv_values('.env')
keys = dict(config)

def connectApi(endPoint=c.PINATAAPIURL+'/data/testAuthentication'):
    try:
        headers = {
        'pinata_api_key': keys['PINATA_API_KEY'],
        'pinata_secret_api_key': keys['PINATA_API_SECRET']      
        }
        r = requests.get(url=endPoint, headers=headers)
        return r
    except:
        raise TypeError('No hay conexion con pinata')

def pinFileToIPFS(path,fileName,type,endPoint=c.PINATAAPIURL+'/pinning/pinFileToIPFS'):
    try:
        headers = {
        'pinata_api_key': keys['PINATA_API_KEY'],
        'pinata_secret_api_key': keys['PINATA_API_SECRET']      
        }
        file_path = path + fileName + '.' + type
        f = open(file_path)
        if f != None:
            file = {'file': open(file_path, 'rb')}
            r = requests.post(url=endPoint, headers=headers, files=file)
            if r.status_code == 200:
                print('El archivo se subio de forma exitosa')
                '''
                Asi responde lo podemos agarrar r.json()["IpfsHash"]
                {
                    IpfsHash: This is the IPFS multi-hash provided back for your content,
                    PinSize: This is how large (in bytes) the content you just pinned is,
                    Timestamp: This is the timestamp for your content pinning (represented in ISO 8601 format)
                }
                '''
                return r
            else:
                raise TypeError(r)
        else:
            raise TypeError('el archivo que tratas de subir no existe')
    except:
        raise TypeError('No hay conexion con pinata')  
    return

def pinListAll(typeFile='json',endPoint=c.PINATAAPIURL+'/data/pinList/?metadata[name]=.'):
    #Aqui optenemos todos los Hash que hemos pingueado
    headers = {
        'pinata_api_key': keys['PINATA_API_KEY'],
        'pinata_secret_api_key': keys['PINATA_API_SECRET']      
    } 
    r = requests.get(url=endPoint + typeFile, headers=headers)
    status = json.loads('{}')
    for i in range(len(r.json()['rows'])):     
        #nameContenido = {'Name': str(r.json()['rows'][i]['metadata']['name'])}
        contenido = { 'Hash'+str(i) : str(r.json()['rows'][i]['ipfs_pin_hash'])}
        status.update(contenido) 
    return status

def unpinFile(hashFile,endPoint=c.PINATAAPIURL+'/pinning/unpin'):
    headers = {
    'pinata_api_key': keys['PINATA_API_KEY'],
    'pinata_secret_api_key': keys['PINATA_API_SECRET']      
    }
    r = requests.delete(url=endPoint+'/'+hashFile, headers=headers)
    print(r)
    if r.status_code == 200:
        print('El archivo se ELIMINO de forma exitosa')
        return r
    else:
        raise TypeError(r.json())
    return
