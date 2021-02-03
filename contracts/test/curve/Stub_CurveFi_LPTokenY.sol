// SPDX-License-Identifier: AGPL V3.0
pragma solidity >=0.6.0 <0.8.0;

import "../TestERC20.sol";



/**
 * @dev Simplified stub to imitate Curve.Fi LP-token
 */
contract Stub_CurveFi_LPTokenY is TestERC20 {
    constructor() public TestERC20("Curve.fi yDAI/yUSDC/yUSDT/yTUSD", "yDAI+yUSDC+yUSDT+yTUSD", 18) {
    }
}