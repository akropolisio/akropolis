// SPDX-License-Identifier: AGPL V3.0
pragma solidity ^0.6.12;

interface ICurve {
    function coins(int128 arg0) external view returns (address);

    function add_liquidity(uint256[4] calldata amounts, uint256 min_mint_amount) external; 

    function add_liquidity(uint256[4] calldata amounts, uint256 min_mint_amount, bool underlying) external;

    function add_liquidity(uint256[3] calldata amounts, uint256 min_mint_amount) external;

    function add_liquidity(uint256[3] calldata amounts, uint256 min_mint_amount, bool underlying) external;

    function add_liquidity(uint256[2] calldata amounts, uint256 min_mint_amount) external;

    function add_liquidity(uint256[2] calldata amounts, uint256 min_mint_amount, bool underlying) external;
}