from eth_account import account
from web3.types import Nonce
from bin import c
import web3 
import json
import asyncio
from web3.middleware  import geth_poa_middleware

#Esta es la direccion de mi smartContract Test
ContractAddress = "0x8F0593D7D1347012C9637466c5cd0aC30bA849Ba"
pathAbi = c.PATHTJSON_ABI

def smart_contract(walletAddressCliente,urlPinataJSON):
    w3=web3.Web3(web3.HTTPProvider(c.URLWEB3))

    #Se supone que esto lo hace un poco mas seguro
    walletAddressCliente = w3.toChecksumAddress(walletAddressCliente)

    print('runing smartcontract...')

    if w3.isConnected() == True:
        print('Estamos conectados en web3')

        #Esto es importante ya que sin esto no logro deployear el contrato cuando estoy en una Tesnet
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)  #  Inject poa middleware 

        with open(pathAbi) as f:
            info_json = json.load(f)
        _abi = info_json["abi"]

        #ABI
        instance = w3.eth.contract(address=ContractAddress, abi=_abi)

        gasPrice = w3.toWei(0, "gwei")

        #Con esto tengo que hacer mas pruebas pero al parecer desde aqui seteamos que el 
        #usuario sea el que absorba el costo del minteo
        value = w3.toWei(0.001, 'ether')
        nonce = w3.eth.getTransactionCount(walletAddressCliente)

        build_transaction = {
        "chainId": 4,
        "gas": 6700000,
        "maxFeePerGas": 10000000000,
        "maxPriorityFeePerGas": 1000000000, 
        "nonce" : nonce 
        }

        URI_JSON = urlPinataJSON
        mint_txn =  instance.functions.CreateNFT(walletAddressCliente,URI_JSON).buildTransaction(build_transaction)
        print("Funcion Contrato: \n", mint_txn)
        return mint_txn

#Esto solo se utiliza cuando queremos hacer caso omiso de cualquier wallet y queremos ocupar
#solo codigo para hacer la transferencia
def signTransaction(w3,transaction,private_key):
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print('Sign transaction OK: ', signed_txn.rawTransaction)

def sendRawTransaction(w3,signed_txn):
    raw_transation = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(w3.toHex(raw_transation))

def runDeploy(walletAddressCliente,urlPinataJSON):
    print('Iniciando Deploy...')
    smartContract = smart_contract(walletAddressCliente,urlPinataJSON)
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(smartContract)
    #loop.close()
    return smartContract