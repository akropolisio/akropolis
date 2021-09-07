// SPDX-License-Identifier: AGPL V3.0
pragma solidity ^0.6.12;

import "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";

interface IWETH is IERC20 {
    function deposit() external payable;
}