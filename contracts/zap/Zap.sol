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

    function shouldAddUnderlying(address swapAddress)
        external
        view
        returns (bool);
}


contract Zap is OwnableUpgradeable, ReentrancyGuardUpgradeable {
    using SafeERC20 for IERC20;
    using SafeMath for uint256;
    using Address for address;

    ICurveRegistry public curveReg;

    address private constant wethTokenAddress =
        0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;

    
    address internal constant ETHAddress =
        0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;
    

    mapping(address => bool) public approvedTargets;


    constructor(
        ICurveRegistry _curveRegistry
    ) public {
        approvedTargets[0xDef1C0ded9bec7F1a1670819833240f027b25EfF] = true;
        curveReg = _curveRegistry;
    }


    /**
        @notice This function adds liquidity to a Curve with ETH or ERC20 tokens
        @param _fromToken The token used for entry (address(0) if ether)
        @param _toToken The token to swap to
        @param _curvePool Curve address for the pool
        @param _amount amount _fromToken to deposit into the curve Pool
        @param _swapTarget Execution target of the swap (0x)
        @param _swapData 0x data field
    */
    function zapIn(
        address _fromToken,
        address _toToken,
        address _curvePool,
        uint256 _amount,
        address _swapTarget,
        bytes calldata _swapData
    ) external payable returns (uint256) {
        //transfer token to this address
        IERC20(_fromToken).safeTransferFrom(msg.sender, address(this), _amount);
        
        //get the token address related to the curve Pool
        
        
        // perform the curve process, add liquidity
        uint256 crvTokensBought = _performCurveZapIn(
            _fromToken,
            _toToken,
            _curvePool,
            _amount,
            _swapTarget,
            _swapData
        );
        

        address curveTokenAddress = curveReg.getTokenAddress(_curvePool);
        // transfer the token to msg.sender
        IERC20(curveTokenAddress).transfer(msg.sender, crvTokensBought);

        return crvTokensBought;
    }


    /**
        @notice This function execute the swap on 0x exchange
        @param _fromToken token address use for entry
        @param _toToken token address to receive
        @param _amount amount _fromToken to sell
        @param _swapTarget address of execution (0x)
        @param swapData , data field from 0x api
        @return amtBought , amount of _toToken receive after the swap      
    */

    function _fillQuote(
        address _fromToken,
        address _toToken,
        uint256 _amount,
        address _swapTarget,
        bytes memory swapData
    ) internal returns (uint256 amtBought) {
        if(_fromToken == _toToken) {
            return _amount;
        }

        if(_fromToken == address(0) && _toToken == wethTokenAddress) {
            IWETH(wethTokenAddress).deposit{value: _amount}();
            return _amount;
        }

        uint256 valueToSend;
        if(_fromToken == address(0)) {
            valueToSend = _amount;
        } else {
            _approveToken(_fromToken, _swapTarget);
        }

        uint256 initBal = _getBalance(_toToken);
        require(approvedTargets[_swapTarget], "Target not Autorizhed");
        (bool success, ) = _swapTarget.call{value: valueToSend}(swapData);
        require(success, "SWAP_CALL_FAILED");
        uint256 finalBal = _getBalance(_toToken);

        amtBought = finalBal - initBal;

       
    }



    //function to deposit on curve Pool
    function _performCurveZapIn(
        address _fromToken,
        address _toToken,
        address _curveSwapAddress,
        uint256 amountToPutIn,
        address _swapTarget,
        bytes memory data
    ) internal returns (uint256 crvTokensBought) {
        // check if _fromToken is already an underlying token 
        (bool isUnderlying, uint8 underlyingIndex) = 
            curveReg.isUnderlyingToken(_curveSwapAddress, _fromToken);
        
        // if _from is underlying join directly the pool, 
        if(isUnderlying) {
            crvTokensBought = _addLiquidityCurve(_curveSwapAddress, amountToPutIn, underlyingIndex);
        } else {
            // swap using 0x exchange for _token
            uint256 tokenBought = 
            _fillQuote(_fromToken, _toToken, amountToPutIn, _swapTarget, data);
            if (_toToken == address(0)) _toToken = ETHAddress;
            
            // check index
            (isUnderlying, underlyingIndex) = curveReg.isUnderlyingToken(_curveSwapAddress, _toToken);

            if (isUnderlying) {
                crvTokensBought = _addLiquidityCurve(_curveSwapAddress, tokenBought, underlyingIndex);
            } else {
                (uint256 tokens, uint8 index) = 
                    _enterMetaPool(_curveSwapAddress, _toToken, tokenBought);

                crvTokensBought = _addLiquidityCurve(_curveSwapAddress, tokens, index);
            }
        }
    }


    function _enterMetaPool(
        address _swapAddress,
        address _toTokenAddress,
        uint256 swapToken
    ) internal returns (uint256 tokenBought, uint8 index) {
        address[4] memory poolTokens = curveReg.getPoolTokens(_swapAddress);
        for (uint8 i=0; i<4; i++) {
            address intermediateSwapAddress = curveReg.getSwapAddress(poolTokens[i]);
            
            if (intermediateSwapAddress != address(0)) {
                (, index) = curveReg.isUnderlyingToken(intermediateSwapAddress, _toTokenAddress);
                tokenBought = _addLiquidityCurve(
                    intermediateSwapAddress,
                    swapToken,
                    index
                );

                return (tokenBought, i);
            }
        }
    }

    //add liquidity to pool depending of number of coins 
    function _addLiquidityCurve(
        address _swapAddress,
        uint256 amount,
        uint8 index
    ) internal returns (uint256 crvTokensBought) {
        address tokenAddress = curveReg.getTokenAddress(_swapAddress);
        address depositAddress = curveReg.getDepositAddress(_swapAddress);
        uint256 initalBalance = _getBalance(tokenAddress);
        address entryToken = curveReg.getPoolTokens(_swapAddress)[index];
        if(entryToken != ETHAddress) {
            IERC20(entryToken).safeIncreaseAllowance(
                address(depositAddress),
                amount
            );
        }
        uint256 numTokens = curveReg.getNumTokens(_swapAddress);
        bool addUnderlying = curveReg.shouldAddUnderlying(_swapAddress);
        
        if(numTokens == 4) {
            uint256[4] memory amounts;
            amounts[index] = amount;
            if(addUnderlying) {
                ICurve(depositAddress).add_liquidity(amounts, 0, true);
            } else {
                ICurve(depositAddress).add_liquidity(amounts, 0);
            }
        } else if (numTokens == 3) {
            uint256[3] memory amounts;
            amounts[index] = amount;
            if(addUnderlying) {
                ICurve(depositAddress).add_liquidity(amounts, 0, true);
            } else {
                ICurve(depositAddress).add_liquidity(amounts, 0);
            }
        } else {
            uint256[2] memory amounts;
            amounts[index] = amount;
            if(addUnderlying) {
                ICurve(depositAddress).add_liquidity(amounts, 0, true);
            } else {
                ICurve(depositAddress).add_liquidity(amounts, 0);
            }
        }

        crvTokensBought = _getBalance(tokenAddress) - initalBalance;

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

    // get token balance
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