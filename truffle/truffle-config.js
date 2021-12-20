require('dotenv').config();
const HDWalletProvider = require('@truffle/hdwallet-provider');
var mnemonic = process.env["MNEMONIC"];
var tokenKey = process.env["INFURA_API_KEY"];

module.exports = {

  networks: {
      development: {
        host: "127.0.0.1",
        port: 8545,
        network_id: "*"
      },
      rinkeby:{
        provider: function() {
          return new HDWalletProvider(mnemonic, "wss://rinkeby.infura.io/ws/v3/" + tokenKey);
        },
        network_id: 4,
        confirmations: 10,
        gas: 6700000,
        gasPrice: 10000000000,
        networkCheckTimeout: 1000000,
        timeoutBlocks: 200,
        addressIndex: 2
      },
      ropsten: {
        provider: () => new HDWalletProvider(process.env.MNEMONIC, "https://ropsten.infura.io/v3/" + process.env.INFURA_API_KEY),
        network_id: 3,
        gas: 3000000,
        gasPrice: 10000000000
      }

  },
  compilers:{
    solc:{
      version: "0.8.0",
      optimizer:{
        enable: true,
        runs: 200
      }  
    }
  }
};
