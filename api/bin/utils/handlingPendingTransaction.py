from bin import c
import web3
import time

def connectWeb3():
    w3=web3.Web3(web3.HTTPProvider(c.URLWEB3))
    return w3

def pendingStatus(TXHash):
    connect = connectWeb3()
    if connect.isConnected() == True:
        loop = True
        intentos = 0
        while(loop):
            try:
                data = connect.eth.get_transaction_receipt(TXHash)
                print('Existe la trasaccion!: ', data.status)
                if data.status == 1:
                    loop = False
                    print('Saliendo de pendingStatus')
                    return {'StatusTransacion': 'Confirmada'}
                else:
                    time.sleep(5)
            except web3.exceptions.TransactionNotFound as e:
                intentos += 1
                print('La trasanccion no existe intento: ' + str(intentos))
                time.sleep(5)
                pass