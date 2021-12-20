import os
import random
from bin import createImage
from bin import makeAtributos
from bin import uploadPinata
from bin import getRandomFile
from bin import c, pd, json
from bin import smartContract
from bin import pendingStatus
import requests

#<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>        
#API
#connectApi()
#unpinFile(hashFile)
#uploadPinata.pinFileToIPFS(path,fileName,type)
#<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>    

if __name__ == '__main__':

    if os.getenv('Minteo') == 'True':
        print('Minteo random...')
        #Aqui creamos las Imagenes Random y las minteamos
        try:
            if os.getenv('walletCliente') != None:
                status = {}
                nameFile = createImage.run()    
                status['NameFile'] = nameFile
                responseImage = uploadPinata.pinFileToIPFS(c.PATHIMAGENES,nameFile,'jpg')
                UriHash=c.PIANATA_GATEWAY + responseImage.json()["IpfsHash"]
                status['UriHash'] = UriHash
                statusAtributos = makeAtributos(name=nameFile,uriHash=UriHash) 
                status['MakeAtributos'] = statusAtributos
                responseMetadaJson = uploadPinata.pinFileToIPFS(c.PATHMETADATA,nameFile,'json')
                status['PinataHash'] = c.PIANATA_GATEWAY +responseMetadaJson.json()["IpfsHash"]
                createJson = json.dumps(status)
                #IMPORTANTE DEPLOY
                r = smartContract.runDeploy(walletAddressCliente=os.getenv('walletCliente'),urlPinataJSON=c.PIANATA_GATEWAY +responseMetadaJson.json()["IpfsHash"])
                DataContract = {
                    'ChainID': str(r['chainId']),
                    'TypeSmart' : r['type'],
                    'To' : r['to'],
                    'DataSmartContract' : r['data'],
                    'UriHash' : UriHash
                    }
                requests.post('http://127.0.0.1:5000/random/api/',params=DataContract)

                #Esto deveria ir a mi base de datos, ya que apartir de ahi es donde
                #el front ve y comprueba el status de la transaccion junto con el file minteado
                print(createJson)
        except createImage.LimiteCreacionImagenes:
            raise
            
    if os.getenv('statusTransaction') == 'True':
        #Aqui es donde comprobamos el status de la transaccion y esperamos a que no conteste el Front
        #para responderle
        DataContract = {
            'StatusTransaction' : 'Pendiente'
        }
        requests.post('http://127.0.0.1:5000/sign/TxHash/',params=DataContract)

        TxHash = os.environ['TxHash']
        status = pendingStatus(TxHash)
        DataContract['StatusTransaction'] = str(status['StatusTransacion'])

        requests.post('http://127.0.0.1:5000/sign/TxHash/',params=DataContract)
        #status['StatusTransacion']


    if os.getenv('DELETE_ALL') == 'True':
        print('Unpin All')
        value = input("Esta seguro que desear borrar todo de PINATA Y/N")
        if value == "Y" or value == "y":
            #Aqui borramos los jpg
            jpgHash = uploadPinata.pinListAll(typeFile='jpg')
            for i in range(len(jpgHash)):
                hash = jpgHash['Hash'+str(i)]
                uploadPinata.unpinFile(hashFile=hash)
            #Aqui borramos los JSON
            jsonHash = uploadPinata.pinListAll(typeFile='json')
            for i in range(len(jsonHash)):
                hash = jsonHash['Hash'+str(i)]
                uploadPinata.unpinFile(hashFile=hash)
            print('Borramos todos los json y jpg')
        else:
            print('Que bueno que no lo borraste')
