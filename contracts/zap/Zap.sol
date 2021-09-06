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


interface ICurve {
    function coins(int128 arg0) external view returns (address);

    function add_liquidity(uint256[4] calldata amounts, uint256 min_mint_amount) external; 

    function add_liquidity(uint256[4] calldata amounts, uint256 min_mint_amount, bool underlying) external;

    function add_liquidity(uint256[3] calldata amounts, uint256 min_mint_amount) external;

    function add_liquidity(uint256[3] calldata amounts, uint256 min_mint_amount, bool underlying) external;

    function add_liquidity(uint256[2] calldata amounts, uint256 min_mint_amount) external;

    function add_liquidity(uint256[2] calldata amounts, uint256 min_mint_amount, bool underlying) external;
}

interface ICurveRegistry {
    function getSwapAddress(address tokenAddress) external view returns (address swapAddress);

    function getTokenAddress(address swapAddress) external view returns (address tokenAddress);

    function getDepositAddress(address swapAddress) external view returns (address depoisitAddress);

    function getPoolTokens(address swapAddress) external view returns (address[4] memory poolTokens);

    function getNumTokens(address swapAddress) external view returns (uint8 numTokens);

    function isUnderlyingToken(address swapAddress, address tokenContractAddress) external view returns (bool, uint8);
}


contract Zap is OwnableUpgradeable, ReentrancyGuardUpgradeable {
    using SafeERC20 for IERC20;
    using SafeMath for uint256;
    using Address for address;

    ICurveRegistry public curveReg;

    address private constant wethTokenAddress =
        0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    

    mapping(address => bool) public approvedTargets;


    constructor(
        ICurveRegistry _curveRegistry
    ) public {
        approvedTargets[0xDef1C0ded9bec7F1a1670819833240f027b25EfF] = true;
        curveReg = _curveRegistry;
    }


    function zapIn(
        address _fromToken,
        address _toToken,
        uint256 _amount,
        address _swapTarget,
        bytes calldata _swapData
    ) external payable returns (uint256) {
        //transfer token to this address
        IERC20(_fromToken).safeTransferFrom(msg.sender, address(this), _amount);
        //initiate the swap via 0x
        uint256 amountToSend = _fillQuote(
            _fromToken,
            _toToken,
            _amount,
            _swapTarget,
            _swapData
        );
        //transfer bought token to user
        IERC20(_toToken).transfer(msg.sender, amountToSend);
    }

    function _fillQuote(
        address _fromTokens,
        address _toTokens,
        uint256 _amount,
        address _swapTarget,
        bytes memory swapData
    ) internal returns (uint256 amtBought) {
        if(_fromTokens == _toTokens) {
            return _amount;
        }

        if(_fromTokens == address(0) && _toTokens == wethTokenAddress) {
            IWETH(wethTokenAddress).deposit{value: _amount}();
            return _amount;
        }

        uint256 valueToSend;
        if(_fromTokens == address(0)) {
            valueToSend = _amount;
        } else {
            _approveToken(_fromTokens, _swapTarget);
        }

        uint256 initBal = _getBalance(_toTokens);
        require(approvedTargets[_swapTarget], "Target not Autorizhed");
        (bool success, ) = _swapTarget.call{value: valueToSend}(swapData);
        require(success, "SWAP_CALL_FAILED");
        uint256 finalBal = _getBalance(_toTokens);

        amtBought = finalBal - initBal;

       
    }


    function _performCurveZapIn(
        address _fromToken,
        address _toToken,
        address _curveSwapAddress,
        uint256 amountToPutIn,
        address _swapTarget,
        bytes memory data
    ) internal returns (uint256 crvTokensBought) {
        uint256 tokensBought = _fillQuote(
            _fromToken,
            _toToken,
            amountToPutIn,
            _swapTarget,
            data
        );

        // (uint256 tokens, uint8 index) = _enterMetaPool(_curveSwapAddress, tokens, index);
    }


    function _enterMetaPool(
        address _swapAddress,
        address _toTokenAddress,
        uint256 swapToken
    ) internal returns (uint256 tokenBought, uint8 index) {
        address[4] memory poolTokens = curveReg.getPoolTokens(_swapAddress);
        for (uint8 i=0; i<4; i++) {
            address intermediateSwapAddress = curveReg.getSwapAddress(poolTokens[i]);
            //todo implement addLiquidity logic with or without underlying token
            if (intermediateSwapAddress != address(0)) {
                (, index) = curveReg.isUnderlyingToken(intermediateSwapAddress, _toTokenAddress);
                tokenBought = _enterCurve(
                    intermediateSwapAddress,
                    swapToken,
                    index
                );

                return (tokenBought, i);
            }
        }
    }


    function _enterCurve(
        address _swapAddress,
        uint256 amount,
        uint8 index
    ) internal returns (uint256 crvTokensBought) {
        address tokenAddress = curveReg.getTokenAddress(_swapAddress);
        address depositAddress = curveReg.getDepositAddress(_swapAddress);
        uint256 initalBalance = _getBalance(tokenAddress);
        address entryToken = curveReg.getPoolTokens(_swapAddress)[index];
        // if(entryToken != ETHAddress) {
            
        // }
    }   
    

    function _approveToken(address _token, address _spender) internal {
        IERC20 token = IERC20(_token);
        if(token.allowance(address(this), _spender) >0) return;
        else {
            token.safeApprove(_spender, type(uint256).max);
        }
    }


    function _approveToken(address _token, address _spender, uint256 _amount) internal {
        IERC20(_token).safeApprove(_spender, 0);
        IERC20(_token).safeApprove(_spender, _amount);
    }


    function _getBalance(address token)
        internal
        view
        returns (uint256 balance)
    {
        if (token == address(0)) {
            balance = address(this).balance;
        } else {
            balance = IERC20(token).balanceOf(address(this));
        }
    }

    receive() external payable {
        require(msg.sender != tx.origin, "Do not send ETH directly");
    }
}