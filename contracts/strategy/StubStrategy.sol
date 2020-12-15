pragma solidity ^0.6.12;
pragma experimental ABIEncoderV2;

import {
    BaseStrategy,
    StrategyParams
} from "@yearnvaults/contracts/BaseStrategy.sol";
import "@openzeppelinV3/contracts/token/ERC20/IERC20.sol";
import "@openzeppelinV3/contracts/math/SafeMath.sol";
import "@openzeppelinV3/contracts/utils/Address.sol";
import "@openzeppelinV3/contracts/token/ERC20/SafeERC20.sol";


contract StubStrategy is BaseStrategy {
    using SafeERC20 for IERC20;
    using Address for address;
    using SafeMath for uint256;

    constructor(address _vault) public BaseStrategy(_vault) {
    }


    //Overrides for BaseStrategy
    function name() external override pure returns (string memory) {
        return "StubCurveStrategy";
    }

    //normalizedBalance
    function estimatedTotalAssets() public override view returns (uint256) {
        //want - token registered in strategy, comes from the Vault
        return want.balanceOf(address(this));
    }

    //Strategy steps
    function prepareReturn(uint256 _debtOutstanding)
        internal
        override
        returns (
            uint256 _profit,
            uint256 _loss,
            uint256 _debtPayment
        )
    {
    }

    function adjustPosition(uint256 _debtOutstanding) internal override {
    }

    //Return funds to the strategy ready to be withdrawn by Vault
    function exitPosition(uint256 _debtOutstanding)
        internal
        override
        returns (uint256 _profit, uint256 _loss, uint256 _debtPayment)
    {
    }

    function liquidatePosition(uint256 _amountNeeded)
        internal
        override
        returns (uint256 _amountFreed)
    {
    }

    function prepareMigration(address _newStrategy) internal override {
    }

    function protectedTokens()
        internal
        override
        view
        returns (address[] memory)
    {}
}