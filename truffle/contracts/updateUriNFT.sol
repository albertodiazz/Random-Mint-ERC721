import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract nftChangeUri is ERC721URIStorage {
    
    uint256 public tokenCounter;
    string public _baseTokenUri;

    event debugMsg(string _msg);

    constructor () public ERC721 ("COLLECTION_NAME", "COLLECTION_TICKER"){
        tokenCounter = 0;
    }

    function _tokenUri(uint256 tokenId) public {
				//Cuesta dinero
        require(_exists(tokenId), 'ERC721 Metadata Uri no existe!');
        emit debugMsg('Existe!');
    }

    function _updateUri(uint256 tokenId,string memory newUri) public {
				//Cuesta dinero
        _tokenUri(tokenId);
        _setTokenURI(tokenId,newUri); 
    }

    function _setBaseUri(string memory uri) public {
        //Cuesta dinero
        _baseTokenUri = uri;
    }

    function createCollectible() public returns (uint256) {
				//Cuesta dinero
        uint256 newItemId = tokenCounter;
        _safeMint(msg.sender, newItemId);
        _setTokenURI(newItemId, _baseTokenUri);
        tokenCounter = tokenCounter + 1;
        return newItemId;
    }
}
