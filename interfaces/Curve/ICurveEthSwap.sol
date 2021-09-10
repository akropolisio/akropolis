// SPDX-License-Identifier: AGPL V3.0
pragma solidity ^0.6.12;
interface ICurveEthSwap {
    function add_liquidity(uint256[2] calldata amounts, uint256 min_mint_amount)
        external
        payable
        returns (uint256);
}