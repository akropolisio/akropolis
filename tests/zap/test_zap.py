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


def test_zap(usdt, akro, akro_owner,  zap, curve_token, curve_swap_address, target, user1):
    parameters = {
            "buyToken": "USDT",
            "sellToken": "AKRO",
            "sellAmount": 10000000000000000000
        }
    request = requests.get(quote, params=parameters)
    data = request.json()
    sellToken = data["sellTokenAddress"]
    buyToken = data["buyTokenAddress"]
    sellAmount = data["sellAmount"]
    buyAmount = data["buyAmount"]
    swapTarget = data["to"]
    dataSwap = data["data"]
    gas_price = data["gasPrice"]
    value = data["value"]
    
    #fund user with akro token
    akro.transfer(user1, sellAmount, {"from": akro_owner})
    akro.approve(zap, sellAmount, {"from": user1})
    akro.approve(swapTarget, sellAmount, {"from": user1})
    usdt.approve(curve_swap_address, buyAmount, {"from": user1})
    #call the zap function
    zap.zapIn(sellToken, buyToken, curve_swap_address, sellAmount, swapTarget, dataSwap, {"from": user1, "gas_price": gas_price, "amount": value})
    assert curve_token.balanceOf(user1) > 0


    
    