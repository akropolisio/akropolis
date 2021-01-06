// SPDX-License-Identifier: MIT

pragma solidity ^0.6.12;

import "@openzeppelinV3/contracts/token/ERC20/IERC20.sol";

import "../../../interfaces/yearnV1/IController.sol";
import "../../../interfaces/yearnV1/IStrategy.sol";
import "../../../interfaces/yearnV1/IVault.sol";
import "../../../interfaces/yearnV1/IWrappedVault.sol";

contract YTestStrategy {
    IERC20 public _want;

    constructor (address _token) public {
        _want = IERC20(_token);
    }
    function want() public view returns (address) {
        return address(_want);
    }

    function deposit() public {

    }

    // NOTE: must exclude any tokens used in the yield
    // Controller role - withdraw should return to Controller
    function withdraw(address) public {

    }

    // Controller | Vault role - withdraw should always return to Vault
    function withdraw(uint256) public {

    }

    function skim() public {

    }

    // Controller | Vault role - withdraw should always return to Vault
    function withdrawAll() public returns (uint256) {
        return 0;
    }

    function balanceOf() public view returns (uint256) {
        return 0;
    }
}