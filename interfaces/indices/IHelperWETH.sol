// SPDX-License-Identifier: AGPL V3.0

pragma solidity >=0.6.0 <0.8.0;
pragma experimental ABIEncoderV2;

interface IHelperWETH {
    function convertWethToEth(address _WETH, uint256 _amount, address payable _recipient) external;
}