// SPDX-License-Identifier: AGPL V3.0
pragma solidity ^0.6.12;

interface ICurve {
    function coins(int128 arg0) external view returns (address);

    function add_liquidity(uint256[4] calldata amounts, uint256 min_mint_amount) external;

    function add_liquidity(
        uint256[4] calldata amounts,
        uint256 min_mint_amount,
        bool underlying
    ) external;

    function add_liquidity(uint256[3] calldata amounts, uint256 min_mint_amount) external;

    function add_liquidity(
        uint256[3] calldata amounts,
        uint256 min_mint_amount,
        bool underlying
    ) external;

    function add_liquidity(uint256[2] calldata amounts, uint256 min_mint_amount) external;

    function add_liquidity(
        uint256[2] calldata amounts,
        uint256 min_mint_amount,
        bool underlying
    ) external;

    function remove_liquidity_one_coin(
        uint256 _amount,
        int128 i,
        uint256 min_amount
    ) external;

    function remove_liquidity_one_coin(
        uint256 _amount,
        int128 i,
        uint256 min_amount,
        bool isUnderlying
    ) external;

    function remove_liquidity_one_coin(
        uint256 _amount,
        uint256 i,
        uint256 min_amount
    ) external;

    function calc_withdraw_one_coin(
        uint256 amount,
        int128 i,
        bool _use_underlying
    ) external view returns (uint256);

    function calc_withdraw_one_coin(uint256 amount, int128 i) external view returns (uint256);

    function calc_withdraw_one_coin(uint256 amount, uint256 i) external view returns (uint256);
}
