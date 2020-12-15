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
import "../../interfaces/IERC20Mintable.sol";

contract StubStrategy is BaseStrategy {
    using SafeERC20 for IERC20;
    using Address for address;
    using SafeMath for uint256;

    address investmentAddr;
    uint256 dumbYield;

    constructor(address _vault, address _investmentAddr, uint256 _dumbYield) public BaseStrategy(_vault) {
        investmentAddr = _investmentAddr;
        dumbYield = _dumbYield;
    }


    //Overrides for BaseStrategy
    function name() external override pure returns (string memory) {
        return "StubCurveStrategy";
    }

    //normalizedBalance
    function estimatedTotalAssets() public override view returns (uint256) {
        //want - token registered in strategy, comes from the Vault
        return want.balanceOf(address(this)).add(want.balanceOf(investmentAddr));
    }

    //Return some yield to the Vault or repay the debt (by demand)
    function prepareReturn(uint256 _debtOutstanding) internal override
        returns (
            uint256 _profit,
            uint256 _loss,
            uint256 _debtPayment
        )
    {
        //No steps to cover debt here. Just keep the yield
        uint256 balance = want.balanceOf(investmentAddr);
        if (balance >= _debtOutstanding) {
            _profit = balance.sub(_debtOutstanding);
        }
        else {
            _loss = _debtOutstanding.sub(balance);
        }
    }

    //Re-investment strategy steps
    function adjustPosition(uint256 _debtOutstanding) internal override {
        //Dumb yield emulating
        IERC20Mintable(address(want)).mint(dumbYield);

        uint256 currentBalance = want.balanceOf(address(this));
        want.transfer(investmentAddr, currentBalance);
    }

    //Return funds to the strategy contract ready to be withdrawn by Vault
    function exitPosition(uint256 _debtOutstanding) internal override
        returns (uint256 _profit, uint256 _loss, uint256 _debtPayment)
    {
        //Return funds from the investment address
        uint256 investedFunds = want.balanceOf(investmentAddr);
        want.transferFrom(investmentAddr, address(this), investedFunds);

        uint256 currentBalance = want.balanceOf(address(this));

        if (currentBalance >= _debtOutstanding) {
            _debtPayment = _debtOutstanding;
            _profit = currentBalance.sub(_debtOutstanding);
        }
        else {
            _debtPayment = currentBalance;
            _loss = _debtOutstanding.sub(currentBalance);
        }
        want.approve(address(vault), currentBalance);
    }

    //Convert some funds into the Vault hosted token (wanted) by demand
    function liquidatePosition(uint256 _amountNeeded)
        internal
        override
        returns (uint256 _amountFreed)
    {
        want.transferFrom(investmentAddr, address(this), _amountNeeded);

        _amountFreed = _amountNeeded;//Here fee should be subtracted
    }

    //Migrate funds to another strategy
    function prepareMigration(address _newStrategy) internal override {
        uint256 investedFunds = want.balanceOf(investmentAddr);
        want.transferFrom(investmentAddr, address(this), investedFunds);

        uint256 currentBalance = want.balanceOf(address(this));
        want.approve(_newStrategy, currentBalance);
    }

    function protectedTokens()
        internal
        override
        view
        returns (address[] memory)
    {}
}