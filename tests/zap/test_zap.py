import pytest
import brownie
import requests, json
from brownie import Contract
from brownie.network.gas.strategies import GasNowScalingStrategy
quote = f"https://api.0x.org/swap/v1/quote"


gas_strategy = GasNowScalingStrategy("standard", increment=1.125, block_duration=2)

@pytest.fixture(scope="module")
def prepare_swap():
    pass

ACCURACY = 2e17


def test_zap(dai, crv, zap, user1, dai_owner, weth_owner, weth, target):
    parameters = {
            "buyToken": "DAI",
            "sellToken": "WETH",
            "sellAmount": 10000000000000000000
        }
    request = requests.get(quote, params=parameters)
    data = request.json()
    sellToken = data["sellTokenAddress"]
    buyToken = data["buyTokenAddress"]
    sellAmount = data["sellAmount"]
    swapTarget = data["to"]
    swapAllowance = data["allowanceTarget"]
    dataSwap = data["data"]
    gas_price = data["gasPrice"]
    value = data["value"]
    # fund the contract first

    # zap.depositETH({"from": user1, "amount": 10e18})
    # weth.approve(zap, amount, {"from": user1})
    # weth.approve(swapAllowance, amount, {"from": user1})
    # zap.fillQuote(sellToken, buyToken, swapAllowance, swapTarget, dataSwap, {"from": user1, "gas_price": gas_price, "amount": value})
    weth.transfer(user1, sellAmount, {"from": weth_owner})
    weth.approve(zap, sellAmount, {"from": user1})
    balanceWehBefore = weth.balanceOf(user1)
    assert balanceWehBefore == sellAmount
    zap.zapIn(sellToken, buyToken, sellAmount, swapTarget, dataSwap, {"from": user1, "amount": value})
    balanceAfter = weth.balanceOf(user1)
    assert balanceAfter == 0
    assert dai.balanceOf(user1) > 0
    assert abs(dai.balanceOf(user1) - data["buyAmount"]) <= ACCURACY
    # assert crv.balanceOf(zap) > 0
    
    