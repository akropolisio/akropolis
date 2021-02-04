// SPDX-License-Identifier: AGPL V3.0

pragma solidity >=0.6.0 <0.8.0;
pragma experimental ABIEncoderV2;

import "./IVaultSavings.sol";

//solhint-disable func-order
interface IVaultSavingsStablecoins is  IVaultSavings {
    function deposit(address[] calldata _vaults, address[][] calldata _tokens, uint256[][] calldata _amounts, uint256[] calldata minBaseAmounts) external returns(uint256[] memory amounts);
    function registerVault(address _vault, address _cfDeposit, uint256 tokensCount) external;
}