// SPDX-License-Identifier: AGPL V3.0
pragma solidity >=0.6.0 <0.8.0;

import "@openzeppelin/contracts/math/SafeMath.sol";
import "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20Burnable.sol";

import "../yTokens/IYErc20.sol";

import "./Stub_CurveFi_SwapY.sol";

/** 
 * @dev Test stub for the implementation of Curve.Fi deposit contract for Y-pool.
 * @dev Original code is located in official repository:
 * https://github.com/curvefi/curve-contract/blob/master/contracts/pools/y/DepositY.vy
 */
contract Stub_CurveFi_DepositY  {
    using SafeMath for uint256;
    using SafeERC20 for IERC20;

    uint256 public constant N_COINS = 4;

    //Curve.Fi Swap address
    address public __curve;
    //Curve.Fi LP token
    address public __token;
    address[N_COINS] __coins;
    address[N_COINS] __underlying;

    constructor(address[N_COINS] memory _coins, address[N_COINS] memory _underlying_coins, address _curve, address _token) public {
        __curve = _curve;
        __token = _token;
        for (uint256 i=0; i < N_COINS; i++){
            __coins[i] = _coins[i];
            __underlying[i] = _underlying_coins[i];
        }
    }

    function add_liquidity (uint256[N_COINS] memory uamounts, uint256 min_mint_amount) public {
        uint256[N_COINS] memory amounts = [uint256(0), uint256(0), uint256(0), uint256(0)];

        for (uint256 i = 0; i < uamounts.length; i++) {
            if (uamounts[i] == 0) continue;

            IERC20(__underlying[i]).safeTransferFrom(msg.sender, address(this), uamounts[i]);

            //Mint if needed
            IERC20(__underlying[i]).approve(__coins[i], uamounts[i]);
            IYErc20(__coins[i]).deposit(uamounts[i]);
            
            amounts[i] = IYErc20(__coins[i]).balanceOf(address(this));
            IERC20(__coins[i]).approve(__curve, amounts[i]);
        }
        Stub_CurveFi_SwapY(__curve).add_liquidity(amounts, min_mint_amount);

        uint256 tokens = IERC20(__token).balanceOf(address(this));
        IERC20(__token).safeTransfer(msg.sender, tokens);
    }
    
    function remove_liquidity (uint256 _amount, uint256[N_COINS] memory min_uamounts) public {
        IERC20(__token).safeTransferFrom(msg.sender, address(this), _amount);
        Stub_CurveFi_SwapY(__curve).remove_liquidity(_amount, [uint256(0), uint256(0), uint256(0), uint256(0)]);
        _send_all(msg.sender, min_uamounts);
    }

    function remove_liquidity_imbalance(uint256[N_COINS] memory uamounts, uint256 max_burn_amount) public {
        uint256[N_COINS] memory amounts = [uint256(0), uint256(0), uint256(0), uint256(0)];

        for (uint256 i = 0; i < uamounts.length; i++) {
            if (uamounts[i] > 0) {
                uint256 rate = IYErc20(__coins[i]).getPricePerFullShare();
                amounts[i] = uamounts[i].mul(1e18).div(rate);
            }
        }

        //Transfrer max tokens in
        uint256 _tokens = IERC20(__token).balanceOf(msg.sender);
        if (_tokens > max_burn_amount) _tokens = max_burn_amount;

        IERC20(__token).safeTransferFrom(msg.sender, address(this), _tokens);

        IERC20(__token).approve(__curve, _tokens);
        Stub_CurveFi_SwapY(__curve).remove_liquidity_imbalance(amounts, max_burn_amount);

        //Transfer unused tokens back
        _tokens = IERC20(__token).balanceOf(address(this));
        IERC20(__token).safeTransfer(msg.sender, _tokens);

        //Unwrap and transfer all the coins we've got
        _send_all(msg.sender, [uint256(0), uint256(0), uint256(0), uint256(0)]);
    }

    function coins(int128 i) public view returns (address) {
        return __coins[uint256(i)];
    }

    function underlying_coins(int128 i) public view returns (address) {
        return __underlying[uint256(i)];
    }

    function underlying_coins() public view returns (address[N_COINS] memory) {
        return __underlying;
    }

    function curve() public view returns (address) {
        return __curve;
    }

    function token() public view returns (address) {
        return __token;
    }

    function _send_all(address _addr, uint256[N_COINS] memory min_uamounts) internal {
        for (uint256 i = 0; i < N_COINS; i++) {
            address _coin = __coins[i];
            uint256 _balance = IYErc20(_coin).balanceOf(address(this));

            if (_balance == 0) { //Do nothing for 0 coins
                continue;
            }

            IYErc20(_coin).withdraw(_balance);

            address _ucoin = __underlying[i];
            uint256 _uamount = IERC20(_ucoin).balanceOf(address(this));
            require(_uamount >= min_uamounts[i], "Not enough coins withdrawn in Deposit");
            IERC20(_ucoin).safeTransfer(_addr, _uamount);
        }        
    }
}