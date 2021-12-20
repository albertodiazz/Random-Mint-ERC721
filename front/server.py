from flask.templating import render_template
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

import os
import subprocess

from werkzeug.datastructures import ContentSecurityPolicy

BASE = 'http://127.0.0.1:5000'


app = Flask(__name__, template_folder='template/')
api = Api(app)
#Esto es de ahuevo necesario si es que quiero recibir POST desde front
#A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
CORS(app)

api_call = reqparse.RequestParser()
api_call.add_argument('get_account', type=str)
api_call.add_argument('sign_TxHash', type=str)

api_call.add_argument('ChainID', action='append')
api_call.add_argument('TypeSmart', action='append')
api_call.add_argument('To', action='append')
api_call.add_argument('DataSmartContract', action='append')
api_call.add_argument('UriHash', action='append')
api_call.add_argument('StatusTransaction', action='append')

class peticiones(Resource):

    def post(self):
        args = api_call.parse_args()
        os.environ['ChainID'] = args['ChainID'][0]
        os.environ['TypeSmart']= args['TypeSmart'][0]
        os.environ['To'] = args['To'][0]
        os.environ['DataSmartContract'] = args['DataSmartContract'][0]
        os.environ['UriHash'] = args['UriHash'][0]

    def put(self):
        print('Minteo')
        args = api_call.parse_args()
        if args['get_account'] != None:
            print(args['get_account'])
            os.environ['walletCliente']=args['get_account']
            os.environ['Minteo']='True'
            subprocess.Popen(['python3','../api/run.py'])
            os.environ['Minteo']='False'
        return 

class firma(Resource):
    def post(self):
        args = api_call.parse_args()
        os.environ['StatusTransaction'] = args['StatusTransaction'][0]

    def put(self):
        print('Comprobando Status de la transaccion...')
        args = api_call.parse_args()
        if args['sign_TxHash'] != None:
            print('Tx mandado desdeFront: ', args['sign_TxHash'])
            os.environ['TxHash'] = args['sign_TxHash']
            os.environ['statusTransaction']='True'
            subprocess.Popen(['python3','../api/run.py'])
            os.environ['statusTransaction']='False'

api.add_resource(peticiones,"/random/api/")
api.add_resource(firma,"/sign/TxHash/")


@app.route('/',methods=['GET', 'POST'])
def index():
    #Esto es super importante ya quue tenemos que limpiar las variables del sistema siempre que comenzemos
    #Pero no todas ya que me ocasiona un desmadre
    #os.environ.clear()
    os.environ['ChainID'] = 'None'
    os.environ['TypeSmart']= 'None'
    os.environ['To']= 'None'
    os.environ['DataSmartContract']= 'None'
    os.environ['UriHash']= 'None'
    os.environ['Minteo']= 'None'
    os.environ['StatusTransaction']= 'None'
    os.environ['walletCliente']= 'None'
    os.environ['TxHash']= 'None'
    print('INDEX')
    return render_template('index.html')

@app.route('/get/statusTransacion/',methods=['GET'])
def statusTxHash():
    return jsonify({
        'StatusTransaction' : os.getenv('StatusTransaction')
        })

@app.route('/data/txn_smart/',methods=['GET'])
def dataToFront():
    print(os.getenv('DataSmartContract'))
    return jsonify({
        'chainId' : os.getenv('ChainID'),
        'type' : os.getenv('TypeSmart'),
        'to' : os.getenv('To'),
        'data': os.getenv('DataSmartContract'),
        'walletCliente': os.getenv('walletCliente'),
        'UriHash' : os.getenv('UriHash'),
        })

if __name__ == "__main__":
    app.run(debug=True)