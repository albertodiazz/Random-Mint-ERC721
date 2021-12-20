// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract Test is ERC721URIStorage {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    constructor() ERC721("Mynft", "Test") {}

    function CreateNFT(address owner, string memory tokenURI)
        public
        returns (uint256)
    {
        _tokenIds.increment();

        uint256 newid = _tokenIds.current();
        _mint(owner, newid);
        _setTokenURI(newid, tokenURI);

        return newid;
    }
    function HellowFromTest() public pure returns (string memory) {
        return 'Hello World BRO!';
    }
}