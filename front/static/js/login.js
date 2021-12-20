const showAccount = document.querySelector('.showAccount');

async function connect() {
    console.log('Connectandos con MetaMask...')
    const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
    //const account = accounts[0];
    //showAccount.innerHTML = account;
  }

  function metamaskReloadCallback()
{
    window.ethereum.on('accountsChanged', (accounts) => {
        console.log('El usuario se conecto:' + accounts)
        window.location.href = 'http://localhost:5000/random/'
    })
    window.ethereum.on('networkChanged', (accounts) => {
        console.log('El usuario cambio de Network')
    })
}

metamaskReloadCallback()

document.getElementById("btn-loginMetaMask").onclick = connect;
  