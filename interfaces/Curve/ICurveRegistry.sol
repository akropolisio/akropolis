// SPDX-License-Identifier: AGPL V3.0
pragma solidity ^0.6.12;

interface ICurveRegistry {
    function getSwapAddress(address tokenAddress) external view returns (address swapAddress);

    function getTokenAddress(address swapAddress) external view returns (address tokenAddress);

    function getDepositAddress(address swapAddress) external view returns (address depoisitAddress);

    function getPoolTokens(address swapAddress) external view returns (address[4] memory poolTokens);

    function getNumTokens(address swapAddress) external view returns (uint8 numTokens);

    function isUnderlyingToken(address swapAddress, address tokenContractAddress) external view returns (bool, uint8);

    function shouldAddUnderlying(address swapAddress) external view returns (bool);
}
