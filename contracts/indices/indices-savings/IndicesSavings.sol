// SPDX-License-Identifier: AGPL V3.0

pragma solidity >=0.6.0 <0.8.0;

pragma experimental ABIEncoderV2;

import "@ozUpgradesV3/contracts/token/ERC20/IERC20Upgradeable.sol";
import "@ozUpgradesV3/contracts/token/ERC20/SafeERC20Upgradeable.sol";
import "@ozUpgradesV3/contracts/utils/AddressUpgradeable.sol";
import "@ozUpgradesV3/contracts/math/SafeMathUpgradeable.sol";
import "@ozUpgradesV3/contracts/access/OwnableUpgradeable.sol";
import "@ozUpgradesV3/contracts/utils/ReentrancyGuardUpgradeable.sol";
import "@ozUpgradesV3/contracts/utils/PausableUpgradeable.sol";
import "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";

import "../../../interfaces/uniswap/IUniswapV2Router02.sol";
import "../../../interfaces/indices/IIndicesSavings.sol";
import "../../../interfaces/indices/IHelperWETH.sol";
import "../../../interfaces/IWETH.sol";
import "../../utils/UniversalERC20.sol";

contract IndicesSavings is IIndicesSavings, OwnableUpgradeable, ReentrancyGuardUpgradeable, PausableUpgradeable {
    uint256 constant MAX_UINT256 = uint256(- 1);

    using SafeERC20Upgradeable  for IERC20Upgradeable;
    using AddressUpgradeable for address;
    using SafeMathUpgradeable for uint256;
    using SafeERC20 for IERC20;
    using UniversalERC20 for IERC20;

    struct IndexInfo {
        bool isActive;
        uint256 blockNumber;
        address lpRouter;
    }

    address[] internal registeredIndices;
    mapping(address => IndexInfo) indices;
    IHelperWETH internal helperWETH;

    /// if_succeeds {:msg "Wrong helper"} _helperWETH != address(0);
    function initialize(address _helperWETH) public initializer {
        __Ownable_init();
        __ReentrancyGuard_init();
        __Pausable_init();
        require(_helperWETH != address(0), "Wrong helper");
        helperWETH = IHelperWETH(_helperWETH);
    }

    /// if_succeeds {:msg "wrong index"} address(_lpIndex) != address(0);
    /// if_succeeds {:msg "wrong token"} address(_tokenIn) != address(0);
    /// if_succeeds {:msg "wrong amount in"} _amountIn > 0;
    /// if_succeeds {:msg "wrong amount out"} _amountOutMin > 0;
    /// if_succeeds {:msg "wrong path"} _path.length > 0;
    /// if_succeeds {:msg "not paid or paid extra"} old(IERC20(_lpIndex).balanceOf(address(this))) == IERC20(_lpIndex).balanceOf(address(this));
    /// if_succeeds {:msg "not paid or paid extra"} !(UniversalERC20.isETH(_tokenIn)) ==> old(UniversalERC20.isETH(_tokenIn) ? 0 : IERC20(_tokenIn).balanceOf(address(this))) == IERC20(_tokenIn).balanceOf(address(this));
    /// if_succeeds {:msg "not paid or paid extra"} (UniversalERC20.isETH(_tokenIn)) ==> old(UniversalERC20.isETH(_tokenIn) ? 0 : address(this).balance) == address(this).balance;
    /// if_succeeds {:msg "not paid or paid extra"} old(IERC20(_lpIndex).balanceOf(address(msg.sender))) < IERC20(_lpIndex).balanceOf(address(msg.sender));
    /// if_succeeds {:msg "not paid or paid extra"} old(IERC20(_lpIndex).balanceOf(address(msg.sender))) + _amountOutMin <= IERC20(_lpIndex).balanceOf(address(msg.sender));
    /// if_succeeds {:msg "not paid or paid extra"} !(UniversalERC20.isETH(_tokenIn)) ==> old(UniversalERC20.isETH(_tokenIn) ? 0 : IERC20(_tokenIn).balanceOf(address(msg.sender))) > IERC20(_tokenIn).balanceOf(address(msg.sender));
    /// if_succeeds {:msg "not paid or paid extra"} !(UniversalERC20.isETH(_tokenIn)) ==> old(UniversalERC20.isETH(_tokenIn) ? 0 : IERC20(_tokenIn).balanceOf(address(msg.sender))) - _amountIn == IERC20(_tokenIn).balanceOf(address(msg.sender));
    function _buy(
        IERC20 _lpIndex,
        IERC20 _tokenIn,
        uint256 _amountIn,
        uint256 _amountOutMin,
        address[] calldata _path
    ) internal {
        require(_amountIn > 0, "Swap zero amount");
        require(isIndexRegistered(address(_lpIndex)), "Index is not Registered");
        require(isIndexActive(address(_lpIndex)), "Index is not Active");
        require(_lpIndex != _tokenIn, "Token is index");

        IUniswapV2Router02 router = IUniswapV2Router02(getRouterForIndex(address(_lpIndex)));
        IWETH weth = IWETH(router.WETH());

        if (_tokenIn.isETH()) {
            weth.deposit { value : _amountIn}();
        } else {
            IERC20(_tokenIn).safeTransferFrom(msg.sender, address(this), _amountIn);
        }

        IERC20 tokenIn = _tokenIn.isETH() ? weth : _tokenIn;
        IERC20(tokenIn).safeIncreaseAllowance(address(router), _amountIn);

        uint256 ownBalanceInIndex = IERC20(_lpIndex).balanceOf(address(this));

        router.swapExactTokensForTokens(
            _amountIn,
            _amountOutMin,
            _path,
            address(this),
            block.timestamp
        );

        uint256 convertedAmount = IERC20(_lpIndex).balanceOf(address(this)).sub(ownBalanceInIndex);
        IERC20(_lpIndex).safeTransfer(msg.sender, convertedAmount);

        emit Buy(address(_lpIndex), convertedAmount, msg.sender, address(_tokenIn), _amountIn);
    }

    /// if_succeeds {:msg "wrong index"} address(_lpIndex) != address(0);
    /// if_succeeds {:msg "wrong token"} address(_tokenOut) != address(0);
    /// if_succeeds {:msg "wrong amount in"} _amountIn > 0;
    /// if_succeeds {:msg "wrong amount out"} _amountOutMin > 0;
    /// if_succeeds {:msg "wrong path"} _path.length > 0;
    /// if_succeeds {:msg "not paid or paid extra"} old(IERC20(_lpIndex).balanceOf(address(this))) == IERC20(_lpIndex).balanceOf(address(this));
    /// if_succeeds {:msg "not paid or paid extra"} !(UniversalERC20.isETH(_tokenOut)) ==> old(UniversalERC20.isETH(_tokenOut) ? 0 : IERC20(_tokenOut).balanceOf(address(this))) == IERC20(_tokenOut).balanceOf(address(this));
    /// if_succeeds {:msg "not paid or paid extra"} (UniversalERC20.isETH(_tokenOut)) ==> old(UniversalERC20.isETH(_tokenOut) ? 0 : address(this).balance) == address(this).balance;
    /// if_succeeds {:msg "not paid or paid extra"} old(IERC20(_lpIndex).balanceOf(address(msg.sender))) > IERC20(_lpIndex).balanceOf(address(msg.sender));
    /// if_succeeds {:msg "not paid or paid extra"} old(IERC20(_lpIndex).balanceOf(address(msg.sender))) - _amountIn == IERC20(_lpIndex).balanceOf(address(msg.sender));
    /// if_succeeds {:msg "not paid or paid extra"} !(UniversalERC20.isETH(_tokenOut)) ==> old(UniversalERC20.isETH(_tokenOut) ? 0 : IERC20(_tokenOut).balanceOf(address(msg.sender))) < IERC20(_tokenOut).balanceOf(address(msg.sender));
    /// if_succeeds {:msg "not paid or paid extra"} !(UniversalERC20.isETH(_tokenOut)) ==> old(UniversalERC20.isETH(_tokenOut) ? 0 : IERC20(_tokenOut).balanceOf(address(msg.sender))) + _amountOutMin >= IERC20(_tokenOut).balanceOf(address(msg.sender));
    /// if_succeeds {:msg "not paid or paid extra"} (UniversalERC20.isETH(_tokenOut)) ==> old(UniversalERC20.isETH(_tokenOut) ? 0 : address(msg.sender).balance) < address(msg.sender).balance;
    /// if_succeeds {:msg "not paid or paid extra"} (UniversalERC20.isETH(_tokenOut)) ==> old(UniversalERC20.isETH(_tokenOut) ? 0 : address(msg.sender).balance) + _amountOutMin <= address(msg.sender).balance;
    function _sell(
        IERC20 _lpIndex,
        IERC20 _tokenOut,
        uint256 _amountIn,
        uint256 _amountOutMin,
        address[] calldata _path
    ) internal {
        require(_amountIn > 0, "Swap zero amount");
        require(isIndexRegistered(address(_lpIndex)), "Index is not Registered");
        require(isIndexActive(address(_lpIndex)), "Index is not Active");
        require(_lpIndex != _tokenOut, "Token is index");

        IUniswapV2Router02 router = IUniswapV2Router02(getRouterForIndex(address(_lpIndex)));
        IWETH weth = IWETH(router.WETH());

        IERC20(_lpIndex).safeTransferFrom(msg.sender, address(this), _amountIn);
        IERC20(_lpIndex).safeIncreaseAllowance(address(router), _amountIn);

        IERC20 tokenOut = _tokenOut.isETH() ? weth : _tokenOut;

        uint256 ownBalanceInToken = IERC20(tokenOut).balanceOf(address(this));

        router.swapExactTokensForTokens(
            _amountIn,
            _amountOutMin,
            _path,
            address(this),
            block.timestamp
        );

        uint256 convertedAmount = IERC20(tokenOut).balanceOf(address(this)).sub(ownBalanceInToken);
        if (_tokenOut.isETH()) {
            IERC20(weth).approve(address(helperWETH), convertedAmount);
            helperWETH.convertWethToEth(address(weth), convertedAmount, msg.sender);
        } else {
            IERC20(tokenOut).safeTransfer(msg.sender, convertedAmount);
        }
        emit Sell(address(_lpIndex), _amountIn, msg.sender, address(tokenOut), convertedAmount);
    }

    /// if_succeeds {:msg "wrong token"} address(_tokenIn) != address(0);
    /// if_succeeds {:msg "not ETH"} !(UniversalERC20.isETH(IERC20(_tokenIn))) ==> msg.value == 0;
    /// if_succeeds {:msg "wrong ETH value"} (UniversalERC20.isETH(IERC20(_tokenIn))) ==> msg.value == _amountIn;
    function buy(
        address _lpIndex,
        address _tokenIn,
        uint256 _amountIn,
        uint256 _amountOutMin,
        address[] calldata _path
    ) external payable override nonReentrant whenNotPaused {
        _buy(IERC20(_lpIndex), IERC20(_tokenIn), _amountIn, _amountOutMin, _path);
    }

    function sell(
        address _lpIndex,
        address _tokenOut,
        uint256 _amountIn,
        uint256 _amountOutMin,
        address[] calldata _path
    ) public override nonReentrant whenNotPaused {
        _sell(IERC20(_lpIndex), IERC20(_tokenOut), _amountIn, _amountOutMin, _path);
    }

    /// if_succeeds {:msg "wrong length of indices"} _lpIndices.length > 0;
    /// if_succeeds {:msg "wrong length of input params"} _lpIndices.length == _tokensIn.length && _lpIndices.length == _amountsIn.length &&_lpIndices.length == _amountsOutMin.length &&_lpIndices.length == _paths.length;
    function buy(
        address[] calldata _lpIndices,
        address[] calldata _tokensIn,
        uint256[] calldata _amountsIn,
        uint256[] calldata _amountsOutMin,
        address[][] calldata _paths
    ) external payable override nonReentrant whenNotPaused {
        uint256 countLpIndices = _lpIndices.length;
        require(
            countLpIndices == _tokensIn.length
            && countLpIndices == _amountsIn.length
            && countLpIndices == _amountsOutMin.length
            && countLpIndices == _paths.length,
            "Size of arrays does not match");

        for (uint256 i = 0; i < _lpIndices.length; i++) {
            _buy(IERC20(_lpIndices[i]), IERC20(_tokensIn[i]), _amountsIn[i], _amountsOutMin[i], _paths[i]);
        }
    }

    /// if_succeeds {:msg "wrong length of indices"} _lpIndices.length > 0;
    /// if_succeeds {:msg "wrong length of input params"} _lpIndices.length == _tokensOut.length && _lpIndices.length == _amountsIn.length &&_lpIndices.length == _amountsOutMin.length &&_lpIndices.length == _paths.length;
    function sell(
        address[] calldata _lpIndices,
        address[] calldata _tokensOut,
        uint256[] calldata _amountsIn,
        uint256[] calldata _amountsOutMin,
        address[][] calldata _paths
    ) external payable override nonReentrant whenNotPaused {
        uint256 countLpIndices = _lpIndices.length;
        require(
            countLpIndices == _tokensOut.length
            && countLpIndices == _amountsIn.length
            && countLpIndices == _amountsOutMin.length
            && countLpIndices == _paths.length,
            "Size of arrays does not match");

        for (uint256 i = 0; i < _lpIndices.length; i++) {
            _sell(IERC20(_lpIndices[i]), IERC20(_tokensOut[i]), _amountsIn[i], _amountsOutMin[i], _paths[i]);
        }
    }

    /// if_succeeds {:msg "wrong input params"} address(_lpIndex) != address(0) && address(_lpRouter) != address(0);
    /// if_succeeds {:msg "not registered"} indices[_lpIndex].isActive && indices[_lpIndex].blockNumber == block.number && indices[_lpIndex].lpRouter == _lpRouter;
    function registerIndex(address _lpIndex, address _lpRouter) external override onlyOwner {
        require(!isIndexRegistered(_lpIndex), "Index is already registered");
        require(_lpRouter != address(0), "Wrong address of router");

        registeredIndices.push(_lpIndex);

        indices[_lpIndex] = IndexInfo({
            isActive : true,
            blockNumber : block.number,
            lpRouter : _lpRouter
            });

        emit IndexRegistered(_lpIndex, _lpRouter);
    }

    /// if_succeeds {:msg "wrong input params"} address(_lpIndex) != address(0) && address(_lpRouter) != address(0);
    /// if_succeeds {:msg "not activated"} indices[_lpIndex].isActive && indices[_lpIndex].blockNumber == block.number && indices[_lpIndex].lpRouter == _lpRouter;
    function activateIndex(address _lpIndex, address _lpRouter) external override onlyOwner {
        require(isIndexRegistered(_lpIndex), "Index is not registered");
        require(_lpRouter != address(0), "Wrong address of router");
        indices[_lpIndex] = IndexInfo({
            isActive : true,
            blockNumber : block.number,
            lpRouter : _lpRouter
            });

        emit IndexActivated(_lpIndex, _lpRouter);
    }

    /// if_succeeds {:msg "wrong index"} address(_index) != address(0);
    /// if_succeeds {:msg "not deactivated"} !indices[_index].isActive && indices[_index].blockNumber == block.number && indices[_index].lpRouter == address(0);
    function deactivateIndex(address _index) external override onlyOwner {
        require(isIndexRegistered(_index), "Index is not registered");

        indices[_index] = IndexInfo({
            isActive : false,
            blockNumber : block.number,
            lpRouter : address(0)
            });

        emit IndexDisabled(_index);
    }

    function pause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }

    //view functions
    function isIndexRegistered(address _lpIndex) public override view returns (bool) {
        for (uint256 i = 0; i < registeredIndices.length; i++) {
            if (registeredIndices[i] == _lpIndex) return true;
        }
        return false;
    }

    function isIndexActive(address _lpIndex) public override view returns (bool) {
        return indices[_lpIndex].isActive;
    }

    function supportedIndices() external override view returns (address[] memory) {
        return registeredIndices;
    }

    function activeIndices() external override view returns (address[] memory _indices) {
        uint256 j = 0;
        for (uint256 i = 0; i < registeredIndices.length; i++) {
            if (indices[registeredIndices[i]].isActive) {
                j = j.add(1);
            }
        }
        if (j > 0) {
            _indices = new address[](j);
            j = 0;
            for (uint256 i = 0; i < registeredIndices.length; i++) {
                if (indices[registeredIndices[i]].isActive) {
                    _indices[j] = registeredIndices[i];
                    j = j.add(1);
                }
            }
        }
    }

    function getRouterForIndex(address _lpIndex) public override view returns (address) {
        return indices[_lpIndex].lpRouter;
    }
}
