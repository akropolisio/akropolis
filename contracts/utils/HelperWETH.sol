// SPDX-License-Identifier: AGPL V3.0

pragma solidity >=0.6.0 <0.8.0;
pragma experimental ABIEncoderV2;

import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "../../../interfaces/IWETH.sol";

contract HelperWETH is ReentrancyGuard {
    address internal lastWETH;

    function convertWethToEth(address _WETH, uint256 _amount, address payable _recipient) nonReentrant external {
        require(_recipient != address(0x0000000000000000000000000000000000000000), "wrong address of recipient");
        lastWETH = _WETH;
        IERC20(_WETH).transferFrom(msg.sender, address(this), _amount);
        IWETH(_WETH).withdraw(_amount);
        _recipient.transfer(_amount);
    }

    fallback() external payable {
        require(lastWETH == msg.sender, "only for converting");
    }
}