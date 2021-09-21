// SPDX-License-Identifier: AGPL V3.0
pragma solidity ^0.6.12;

import "@ozUpgradesV3/contracts/access/OwnableUpgradeable.sol";
import "@ozUpgradesV3/contracts/token/ERC20/SafeERC20Upgradeable.sol";
import "@ozUpgradesV3/contracts/math/SafeMathUpgradeable.sol";
import "@ozUpgradesV3/contracts/utils/ReentrancyGuardUpgradeable.sol";

import "@ozUpgradesV3/contracts/utils/PausableUpgradeable.sol";

import "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";

import "../../interfaces/Curve/ICurve.sol";
import "../../interfaces/Curve/ICurveRegistry.sol";

import "../../interfaces/Curve/ICurveEthSwap.sol";

import "../../interfaces/IWETH.sol";

import "../../interfaces/VaultSavings/IVaultSavingsV2.sol";

contract Zap is OwnableUpgradeable, ReentrancyGuardUpgradeable, PausableUpgradeable {
    using SafeERC20 for IERC20;
    using SafeMath for uint256;

    ICurveRegistry public curveReg;

    IVaultSavingsV2 public vaultsavings;

    address private constant wethTokenAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;

    address internal constant ETHAddress = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;

    mapping(address => bool) public approvedTargets;

    mapping(address => bool) public approvedTokens;

    event ZapIn(address sender, address vault, uint256 tokensRec);

    event ZapOut(address sender, address token, uint256 tokensRec);

    event AddLiquidity(address sender, address token, uint256 amount);


    function initialize(ICurveRegistry _curveRegistry, IVaultSavingsV2 _vault) virtual public initializer {
        __Ownable_init();
        __Pausable_init();
        __ReentrancyGuard_init();
        approvedTargets[0xDef1C0ded9bec7F1a1670819833240f027b25EfF] = true;
        curveReg = _curveRegistry;
        vaultsavings = _vault;
    }

    /**
        @notice This function adds liquidity to a Curve with ETH or ERC20 tokens
        @param _fromToken The token used for entry (address(0) if ether)
        @param _toToken The token to swap to
        @param _curvePool Curve address for the pool
        @param _amount amount _fromToken to deposit into the curve Pool
        @param _swapTarget Execution target of the swap (0x)
        @param _vault address of yearn vault
        @param _swapData 0x data field
    */
    function zapIn(
        address _fromToken,
        address _toToken,
        address _curvePool,
        uint256 _amount,
        uint256 _minPoolAmount,
        address _swapTarget,
        address _vault,
        bytes calldata _swapData
    ) external payable returns (uint256 yearnLp) {

        if(_fromToken == address(0)) {
            _fromToken = ETHAddress;
        } else {
            require(_amount > 0, "amount can't be empty");
            require(approvedTokens[_fromToken], "token isn't allowed for zap");
            IERC20(_fromToken).safeTransferFrom(msg.sender, address(this), _amount);
        }

        // perform the curve process, add liquidity
        uint256 crvTokensBought = _performCurveZapIn(_fromToken, _toToken, _curvePool, _amount, _swapTarget, _swapData);
        

        require(crvTokensBought >= _minPoolAmount, "slippage error");
        

        address curveTokenAddress = curveReg.getTokenAddress(_curvePool);

        uint256 iniBalance = IERC20(_vault).balanceOf(address(this));
        // approve vault deposit
        IERC20(curveTokenAddress).approve(address(vaultsavings), crvTokensBought);
        // deposit to yearn vault
        vaultsavings.deposit(_vault, crvTokensBought);

        // remove approval
        IERC20(curveTokenAddress).approve(address(vaultsavings), 0);

        yearnLp = IERC20(_vault).balanceOf(address(this)).sub(iniBalance);

        // transfer lp yearn to msg.sender
        require(yearnLp > 0, "zap failed");

        IERC20(_vault).transfer(msg.sender, yearnLp);

        emit ZapIn(msg.sender, _vault, yearnLp);
    }

    /**
        @notice this function unstake from deposit vault and perform a zapOut on curve
        @param _swapAddress curve swap address
        @param _vault yearn vault
        @param yLpToken amount of yearn shares
        @param _swapTarget Execution target of the swap (0x)
        @param _toToken token in which we convert
        @param _fromToken token to exit the pool
        @param _swapData data field from 0x_API
        @return toTokensBought indicates the amount of toToken received  
    */

    function zapOut(
        address _swapAddress,
        address _vault,
        uint256 yLpToken,
        uint256 _min_toToken,
        address _swapTarget,
        address _fromToken,
        address _toToken,
        bytes calldata _swapData
    ) external payable returns (uint256 toTokensBought) {
        
        require(approvedTokens[_toToken], "token isn't allowed for zap");

        address tokenAdress = curveReg.getTokenAddress(_swapAddress);

        uint256 crvAmount = withdrawFromVault(_vault, yLpToken, tokenAdress);

        toTokensBought = _performCurveZapOut(_swapAddress, crvAmount, _fromToken, _toToken, _swapTarget, _swapData);


        require(toTokensBought > _min_toToken, "slippage error");
        //transfer token receive to user
        IERC20(_toToken).transfer(msg.sender, toTokensBought);

        emit ZapOut(msg.sender, _toToken, toTokensBought);
    }


    function withdrawFromVault(address _vault, uint256 yLpToken, address _token) internal returns (uint256 crvBalance){
        uint256 iniBalance = _getBalance(_token);

        //transfer lpToken to zapContract
        IERC20(_vault).transferFrom(msg.sender, address(this), yLpToken);

        // approve vault savings
        IERC20(_vault).approve(address(vaultsavings), yLpToken);

        vaultsavings.withdraw(_vault, yLpToken);

        // remove approval
        IERC20(_vault).approve(address(vaultsavings), 0);

        crvBalance = _getBalance(_token).sub(iniBalance);
            
    }




    /**
        @notice update the registry
        @param newRegistry , new registry to point to
    */
    function updateRegistry(ICurveRegistry newRegistry) external onlyOwner {
        require(newRegistry != curveReg, "already used");
        curveReg = newRegistry;
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

        if (_fromToken == _toToken) {
            return _amount;
        }

        if (
            _fromToken == wethTokenAddress &&
            _toToken == address(0)
        ) {
            IWETH(wethTokenAddress).withdraw(_amount);
            return _amount;
        } else if (
            _fromToken == address(0) &&
            _toToken == wethTokenAddress
        ) {
            IWETH(wethTokenAddress).deposit{ value: _amount }();
            return _amount;
        }

        uint256 valueToSend;
        if (_fromToken == address(0)) {
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
        require(amtBought > 0, "invalid token");
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
        (bool isUnderlying, uint8 underlyingIndex) = curveReg.isUnderlyingToken(_curveSwapAddress, _fromToken);

        // if _from is underlying join directly the pool,
        if (isUnderlying) {
            crvTokensBought = _addLiquidityCurve(_curveSwapAddress, amountToPutIn, underlyingIndex);
        } else {
            // swap using 0x exchange for _token
            uint256 tokenBought = _fillQuote(_fromToken, _toToken, amountToPutIn, _swapTarget, data);
            if (_toToken == address(0)) _toToken = ETHAddress;

            // check index
            (isUnderlying, underlyingIndex) = curveReg.isUnderlyingToken(_curveSwapAddress, _toToken);

            if (isUnderlying) {
                crvTokensBought = _addLiquidityCurve(_curveSwapAddress, tokenBought, underlyingIndex);
            } else {
                (uint256 tokens, uint8 index) = _enterMetaPool(_curveSwapAddress, _toToken, tokenBought);

                crvTokensBought = _addLiquidityCurve(_curveSwapAddress, tokens, index);
            }
        }
    }

    /**
        @notice perform the zapout from curve pool
        @param _swapAddress curve swap address
        @param amountCrv amount of crvToken we use to swap
        @param _fromToken token in which we exit the pool
        @param _toToken token to which we convert
        @param _swapTarget address of execution (0x)
        @param _swapData , data field from 0x api
    */
    function _performCurveZapOut(
        address _swapAddress,
        uint256 amountCrv,
        address _fromToken,
        address _toToken,
        address _swapTarget,
        bytes memory _swapData
    ) internal returns (uint256) {
        (bool isUnderlying, uint256 index) = curveReg.isUnderlyingToken(_swapAddress, _fromToken);

        if (isUnderlying) {
            uint256 _fromTokenBought = _removeLiquidityCurve(_swapAddress, amountCrv, index, _fromToken);

            if (_fromToken == ETHAddress) _fromToken = address(0);

            uint256 toTokenBought = _fillQuote(_fromToken, _toToken, _fromTokenBought, _swapTarget, _swapData);

            return toTokenBought;
        } else {
            address[4] memory poolTokens = curveReg.getPoolTokens(_swapAddress);
            address swap;
            uint8 i;
            for (; i < 4; i++) {
                swap = curveReg.getSwapAddress(poolTokens[i]);
                break;
            }
            uint256 crvBought = _exitMetaPool(_swapAddress, amountCrv, i, poolTokens[i]);

            uint256 toTokenBought = _performCurveZapOut(swap, crvBought, _fromToken, _toToken, _swapTarget, _swapData);
            return toTokenBought;
        }
    }

    function _enterMetaPool(
        address _swapAddress,
        address _toTokenAddress,
        uint256 swapToken
    ) internal returns (uint256 tokenBought, uint8 index) {
        address[4] memory poolTokens = curveReg.getPoolTokens(_swapAddress);
        for (uint8 i = 0; i < 4; i++) {
            address intermediateSwapAddress = curveReg.getSwapAddress(poolTokens[i]);

            if (intermediateSwapAddress != address(0)) {
                (, index) = curveReg.isUnderlyingToken(intermediateSwapAddress, _toTokenAddress);
                tokenBought = _addLiquidityCurve(intermediateSwapAddress, swapToken, index);

                return (tokenBought, i);
            }
        }
    }

    /**
        @notice remove liquitidy from metapools curve
        @param _swapAddress address of the curve pool 
        @param _amountCRV amount of liquidity to remove
        @param index , position of underlying token to remove
        @param _toToken token to convert after exit
    */
    function _exitMetaPool(
        address _swapAddress,
        uint256 _amountCRV,
        uint256 index,
        address _toToken
    ) internal returns (uint256) {
        //get the crvToken of the pool
        address tokenAddress = curveReg.getTokenAddress(_swapAddress);

        _approveToken(tokenAddress, _swapAddress);

        //balance of _toToken on the contract
        uint256 iniTokenBalance = IERC20(_toToken).balanceOf(address(this));

        //remove liquidity from curve pool
        ICurve(_swapAddress).remove_liquidity_one_coin(_amountCRV, int128(index), 0);

        //token receive after remove liquidity
        uint256 tokenReceived = (IERC20(_toToken).balanceOf(address(this))).sub(iniTokenBalance);

        require(tokenReceived > 0, "fail");

        return tokenReceived;
    }

    /**
        @notice add liquidity to curve pool
        @param _swapAddress curve swap address
        @param amount amount to invest
        @param index position of token
        @return crvTokensBought amount of lp token received 
    */
    function _addLiquidityCurve(
        address _swapAddress,
        uint256 amount,
        uint8 index
    ) internal returns (uint256 crvTokensBought) {
        address tokenAddress = curveReg.getTokenAddress(_swapAddress);
        address depositAddress = curveReg.getDepositAddress(_swapAddress);
        uint256 initalBalance = _getBalance(tokenAddress);
        address entryToken = curveReg.getPoolTokens(_swapAddress)[index];
        if (entryToken != ETHAddress) {
            IERC20(entryToken).safeIncreaseAllowance(address(depositAddress), amount);
        }
        uint256 numTokens = curveReg.getNumTokens(_swapAddress);
        bool addUnderlying = curveReg.shouldAddUnderlying(_swapAddress);

        if (numTokens == 4) {
            uint256[4] memory amounts;
            amounts[index] = amount;
            if (addUnderlying) {
                ICurve(depositAddress).add_liquidity(amounts, 0, true);
            } else {
                ICurve(depositAddress).add_liquidity(amounts, 0);
            }
        } else if (numTokens == 3) {
            uint256[3] memory amounts;
            amounts[index] = amount;
            if (addUnderlying) {
                ICurve(depositAddress).add_liquidity(amounts, 0, true);
            } else {
                ICurve(depositAddress).add_liquidity(amounts, 0);
            }
        } else {
            uint256[2] memory amounts;
            amounts[index] = amount;
            // get if pool is an Eth pool and send msgvalue to the contract
            if(curveReg.isEthPool(depositAddress)){
                ICurveEthSwap(depositAddress).add_liquidity{value: amount}(amounts, 0);
            } else if (addUnderlying) {
                ICurve(depositAddress).add_liquidity(amounts, 0, true);
            } else {
                ICurve(depositAddress).add_liquidity(amounts, 0);
            }
        }

        crvTokensBought = _getBalance(tokenAddress) - initalBalance;

        
    }

    /**
        @notice remove liquidity from curve pool
        @param _swapAddress address of curve swap
        @param crvToken amount of lpToken to burn
        @param index position of token to get back
        @param toToken token to withdraw
        @return tokenReceived amout of toToken received
    */

    function _removeLiquidityCurve(
        address _swapAddress,
        uint256 crvToken,
        uint256 index,
        address toToken
    ) internal returns (uint256 tokenReceived) {
        address depositAddress = curveReg.getDepositAddress(_swapAddress);

        address tokenAddress = curveReg.getTokenAddress(_swapAddress);

        _approveToken(tokenAddress, depositAddress);

        address bToken = toToken == ETHAddress ? address(0) : toToken;

        uint256 iniBalance = _getBalance(bToken);

        if (curveReg.shouldAddUnderlying(_swapAddress)) {
            ICurve(depositAddress).remove_liquidity_one_coin(crvToken, int128(index), 0, true);
        } else {
            ICurve(depositAddress).remove_liquidity_one_coin(crvToken, index, 0);
        }

        tokenReceived = _getBalance(bToken).sub(iniBalance);

        require(tokenReceived > 0, "remove liquidity failed");
    }

    /**
        @notice approve token max unlimited supply
        @param _token address of token we work with
        @param _spender address to approve for
    */
    function _approveToken(address _token, address _spender) internal {
        IERC20 token = IERC20(_token);
        if (token.allowance(address(this), _spender) > 0) return;
        else {
            token.safeApprove(_spender, type(uint256).max);
        }
    }

    /**
        @notice approve token max limited supply
        @param _token address of token we work with
        @param _spender address to approve for
        @param _amount amount to approve
    */
    function _approveToken(
        address _token,
        address _spender,
        uint256 _amount
    ) internal {
        IERC20(_token).safeApprove(_spender, 0);
        IERC20(_token).safeApprove(_spender, _amount);
    }

    // get token balance
    function _getBalance(address token) internal view returns (uint256 balance) {
        if (token == address(0)) {
            balance = address(this).balance;
        } else {
            balance = IERC20(token).balanceOf(address(this));
        }
    }

    function setApprovedTokens(
        address[] calldata tokens,
        bool[] calldata isApproved
    ) external onlyOwner {
        require(tokens.length == isApproved.length, "Invalid Input length");

        for (uint256 i = 0; i < tokens.length; i++) {
            approvedTokens[tokens[i]] = isApproved[i];
        }
    }

    receive() external payable {
        require(msg.sender != tx.origin, "Do not send ETH directly");
    }
}