function msg_Felicidad(url){
  var img = document.createElement("img");
  img.src = url;
  var src = document.getElementById("header");
  src.appendChild(img);
  document.getElementById("Felicidades").hidden = false

}

async function Minteando(response){
  console.log('Firmando contrato')
  const from_ = response['walletCliente']
  const urihash = response['UriHash']

  let msgParams = {
    value: '0', 
    type: response['type'], 
    chainId: parseInt(response['chainId']), 
    gas: '60000', 
    nonce: 0, 
    to:  response['to'], 
    data: response['data']
  };
  msgParams.from = from_
  try {
    const sign = await ethereum.request({
      method: 'eth_sendTransaction',
      params: [msgParams],
    });
    //Una vez que se haya firmanado nos dara un txhash de la transaccion en ese momento la enviamos
    //a nuestro back para que maneje la peticion pendiente y nos confirme cuando se haya realizado
    console.log(sign)
    var params = {"sign_TxHash":sign};
    var data = JSON.stringify(params)
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "PUT", 'http://127.0.0.1:5000/sign/TxHash/', true); // false for synchronous request
    xmlHttp.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xmlHttp.send(data);

    var r = await makeGetRequestStatusTransaction();

  } catch (err) {
    console.error(err);
  }
 
}

async function makeGetRequest(){
  path = "http://127.0.0.1:5000/data/txn_smart/"
  var loop = window.setTimeout(makeGetRequest,5000);
  return new Promise( function (resolve, reject) {
    axios.get(path).then(
        (response) => {
            var result = response.data;
            console.log('Processing Request');
            console.log(result)
            if (result['data'] != 'None'){
              document.getElementById("WAIT").hidden = true
              document.getElementById("STATUS").hidden = false
              Minteando(result)
              clearTimeout(loop);
            }
            resolve(result);
        },
            (error) => {
            reject(error);
        }
    );
});
}

function getData() {
  return new Promise(function (resolve) {
  axios.get('http://127.0.0.1:5000/data/txn_smart/').then(
    (response) => {
    resolve(response.data);
  });
});}

async function makeGetRequestStatusTransaction(response){
  path = "http://127.0.0.1:5000/get/statusTransacion/"
  var loop = window.setTimeout(makeGetRequestStatusTransaction,5000);
  return new Promise( function (resolve, reject) {
    axios.get(path).then(
        (response) => {
            var result = response.data;
            console.log('Processing Request Status transaction');
            console.log(result)
            if(result['StatusTransaction']=="Confirmada"){
                var dataSmart = getData();
                if (dataSmart != undefined){
                  document.getElementById("STATUS").hidden = true
                  console.log('Ha sido confirmada');
                  dataSmart.then(function(resultSmart){ 
                    console.log(resultSmart.UriHash)
                    msg_Felicidad(resultSmart.UriHash)
                    clearTimeout(loop);
                  });
                }
            }
            resolve(result['StatusTransaction']);
        },
            (error) => {
            reject(error);
        }
    );
});
}

async function generandoImagen(){
  console.log('random image')
  
  const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
  const account = accounts[0];
  
  var params = {"get_account":account};
  var data = JSON.stringify(params)

  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "PUT", 'http://127.0.0.1:5000/random/api/', true); // false for synchronous request
  xmlHttp.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  xmlHttp.send(data);

  document.getElementById("btn-RandomMint").hidden = true
  
  document.getElementById("WAIT").hidden = false
  var Response = await makeGetRequest();
  
  return xmlHttp.responseText;
}

document.getElementById("Felicidades").hidden = true
document.getElementById("WAIT").hidden = true
document.getElementById("STATUS").hidden = true
document.getElementById("btn-RandomMint").onclick = generandoImagen;


 //OCUPAR FETCH