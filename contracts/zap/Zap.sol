// SPDX-License-Identifier: AGPL V3.0
pragma solidity ^0.6.12;

import "@ozUpgradesV3/contracts/access/OwnableUpgradeable.sol";
import "@ozUpgradesV3/contracts/token/ERC20/SafeERC20Upgradeable.sol";
import "@ozUpgradesV3/contracts/math/SafeMathUpgradeable.sol";
import "@ozUpgradesV3/contracts/utils/ReentrancyGuardUpgradeable.sol";

import "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";



interface IWETH is IERC20 {
    function deposit() external payable;
}


contract Zap is OwnableUpgradeable, ReentrancyGuardUpgradeable {
    using SafeERC20 for IERC20;
    using SafeMath for uint256;
    using Address for address;

    IWETH public immutable WETH;
    constructor(
        IWETH weth
    ) public {
        WETH = weth;
    }

    
    /**
    @dev Must attach ETH equal to the `value` field from the API response.
    @param sellAddress 'sellAddress' from the API response
    @param buyAddress The 'buyAddress' field from the API response
    @param sellQuantity The 'sellAmount' field from the API response
    @param zapContract The 'to' field from the API response
    @param data The 'data' field from the API response
    */
    function ZapIn(
        IERC20 sellAddress,
        IERC20 buyAddress,
        uint256 sellQuantity,
        address payable zapContract,
        bytes calldata data
    ) external payable returns (uint256) {
        if(address(sellAddress) != address(0)) {
            IERC20(sellAddress).safeTransferFrom(
                msg.sender,
                address(this),
                sellQuantity
            );
        }

        uint256 tokenReceive = _fillQuote(
            sellAddress,
            buyAddress,
            zapContract,
            data
        );

        if (address(buyAddress) != address(0)) {
            _withdrawToken(buyAddress, tokenReceive);
        } else {
            _withdrawETH(tokenReceive);
        }
    }



    // Swaps ERC20->ERC20 tokens held by this contract using a 0x-API quote.
    function _fillQuote(
        // The `sellTokenAddress` field from the API response.
        IERC20 sellToken,
        // The `buyTokenAddress` field from the API response.
        IERC20 buyToken,
        // The `to` field from the API response.
        address payable swapTarget,
        // The `data` field from the API response.
        bytes calldata swapCallData 
    ) internal returns (uint256) {
        // Track our balance of the buyToken to determine how much we've bought.
        uint256 boughtAmount = buyToken.balanceOf(address(this));
        // Give `spender` an infinite allowance to spend this contract's `sellToken`.
        // Note that for some tokens (e.g., USDT, KNC), you must first reset any existing
        // allowance to 0 before being able to update it.]
        require(sellToken.approve(swapTarget, uint256(-1)));

        (bool success, ) = swapTarget.call{value: msg.value}(swapCallData);
        require(success, "SWAP_FAILED");

        // Refund any unspent protocol fees to the sender.
        msg.sender.transfer(address(this).balance);
        // Use our current buyToken balance to determine how much we've bought.
        boughtAmount = buyToken.balanceOf(address(this)).sub(boughtAmount);

        return boughtAmount;
    }

        // Transfer tokens held by this contrat to the sender/owner.
    function _withdrawToken(IERC20 token, uint256 amount)
        internal
        
    {
        require(token.transfer(msg.sender, amount));
    }

    // Transfer ETH held by this contrat to the sender/owner.
    function _withdrawETH(uint256 amount)
        internal
    {
        msg.sender.transfer(amount);
    }

    // Payable fallback to allow this contract to receive protocol fee refunds.
    receive() external payable {}


    // Transfer ETH into this contract and wrap it into WETH.
    function depositETH()
        external
        payable
    {
        WETH.deposit{value: msg.value}();
    }
    
}