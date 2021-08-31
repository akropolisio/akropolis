import pytest
import brownie
import requests, json
from brownie import Contract
amount = 10e18
quote = f"https://api.0x.org/swap/v1/quote"

@pytest.fixture(scope="module")
def prepare_swap():
    pass



def test_zap(dai, crv, zap, user1, dai_owner, target):
    parameters = {
            "buyToken": "DAI",
            "sellToken": "CRV",
            "buyAmount": 100000000
        }
    request = requests.get(quote, params=parameters)
    data = request.json()
    need = data["data"]
    dai.transfer(user1, amount, {"from": dai_owner})
    balanceSellBefore = dai.balanceOf(user1)
    balanceBuyBefore = crv.balanceOf(user1)
    assert balanceSellBefore == amount
    assert balanceBuyBefore == 0
    
    dai.approve(zap, amount, {"from": user1})
    zap.ZapIn(dai, crv, amount, target, need, {"from": user1})
    assert dai.balanceOf(user1) == 0
    assert crv.balanceOf(user1) > 0
    