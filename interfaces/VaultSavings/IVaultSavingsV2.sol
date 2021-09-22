// SPDX-License-Identifier: AGPL V3.0

pragma solidity >=0.6.0 <0.8.0;

interface IVaultSavingsV2 {
    function deposit(address _vault, uint256 _amount) external returns (uint256);

    function withdraw(address _vault, uint256 _amount) external returns (uint256);

    function balanceOf(address _sender) external returns (uint256);
}
