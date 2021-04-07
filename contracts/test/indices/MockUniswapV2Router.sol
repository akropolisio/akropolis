// SPDX-License-Identifier: AGPL V3.0

pragma solidity >=0.6.0;

import "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract MockUniswapV2Router {
    using SafeERC20 for IERC20;

    address public WETH;

    struct Amounts {
        uint amountA;
        uint amountB;
    }
    mapping(address => mapping(address => Amounts)) internal pairs;
    mapping(address => bool) internal wrongPath;

    constructor(address _weth) public {
        WETH = _weth;
    }

    function swapExactTokensForTokens(
        uint amountIn,
        uint amountOutMin,
        address[] calldata path,
        address to,
        uint deadline
    ) external returns (uint[] memory amounts) {
        require(path.length >= 2, "wrong path");
        amounts = getAmountsOut(amountIn, path);
        require( amounts[amounts.length - 1] >= amountOutMin, "mock small price");
        IERC20(path[0]).safeTransferFrom(msg.sender, address(this), amountIn);
        IERC20(path[path.length - 1]).transfer(msg.sender, amounts[amounts.length - 1]);
    }

    function getAmountsOut(uint amountIn, address[] memory path)
    public
    view
    returns (uint[] memory amounts)
    {
        require(path.length >= 2, "wrong path");
        address tokenA = path[0];
        address tokenB = path[path.length - 1];
        require(pairs[tokenA][tokenB].amountA > 0 && pairs[tokenA][tokenB].amountB > 0, "wrong pair");
        uint amount = amountIn * pairs[tokenA][tokenB].amountB / pairs[tokenA][tokenB].amountA;
        require(amount > 0, "wrong amount");
        amounts = new uint[](path.length);
        for (uint i; i < path.length - 1; i++) {
            require(wrongPath[path[i]] == false, "mock wrong path");
            amounts[i + 1] = amount;
        }
        amounts[0] = amountIn;
    }

    function mockAddLiquidity(
        address tokenA,
        address tokenB,
        uint amountA,
        uint amountB
    ) external {
        require(amountA > 0);
        require(amountB > 0);
        pairs[tokenA][tokenB] = Amounts(amountA, amountB);
        pairs[tokenB][tokenA] = Amounts(amountB, amountA);
    }

    function addWrongPath(
        address middleToken
    ) external {
        wrongPath[middleToken] = true;
    }
}
