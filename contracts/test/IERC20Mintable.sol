// SPDX-License-Identifier: AGPL V3.0
pragma solidity >=0.6.0 <0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IERC20Mintable is IERC20 {
    function mint(address account, uint256 amount) external returns (bool);
}