// SPDX-License-Identifier: MIT

pragma solidity ^0.6.12;

import "./ICurveFiDeposit.sol";

interface ICurveFiDeposit4 is ICurveFiDeposit { 
    function add_liquidity (uint256[4] calldata uamounts, uint256 min_mint_amount) external;
    function remove_liquidity (uint256 _amount, uint256[4] calldata min_uamounts) external;
    function remove_liquidity_imbalance (uint256[4] calldata uamounts, uint256 max_burn_amount) external;
}