// SPDX-License-Identifier: AGPL V3.0
pragma solidity >=0.6.0 <0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "./IERC20Mintable.sol";

contract TestERC20 is ERC20, IERC20Mintable {
    constructor(string memory name, string memory symbol, uint8 _decimals) public ERC20(name, symbol) {
        _setupDecimals(_decimals);
    }

    function mint(uint256 amount) external returns (bool) {
        _mint(_msgSender(), amount);
        return true;
    }

    function mint(address account, uint256 amount) external override returns (bool) {
        _mint(account, amount);
        return true;
    }
    
    function allocateTo(address account, uint256 amount) external {
        _mint(account, amount);
    } 

}