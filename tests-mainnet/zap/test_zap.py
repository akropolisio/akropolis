import pytest
import brownie
from brownie import accounts
import requests, json
from brownie import Contract
import parametrize_from_file

quote = f"https://api.0x.org/swap/v1/quote"


data = "./data/data.json"

#this test is for token with low price value
@parametrize_from_file(data, "data_zap_low")
def test_zap_high_liquidity(
    zap, user1, yearn_vault, sellTokenName, buyTokenName, whale, curve_address
):
    curve_swap_address = Contract.from_explorer(curve_address, as_proxy_for=None)
    vault = Contract.from_explorer(yearn_vault, as_proxy_for=None)
    token_whale = accounts.at(whale, force=True)
    parameters1 = {
        "buyToken": buyTokenName,
        "sellToken": sellTokenName,
        #we will change amount in the different price test
        "sellAmount": 1000000000000000000000000,
    }
    request1 = requests.get(quote, params=parameters1)
    data1 = request1.json()
    sellToken = data1["sellTokenAddress"]
    buyToken = data1["buyTokenAddress"]
    sellAmount = data1["sellAmount"]
    buyAmount = data1["buyAmount"]
    swapTarget = data1["to"]
    dataSwap = data1["data"]
    gas_price = data1["gasPrice"]
    value = data1["value"]

    tokenToSell = Contract.from_explorer(sellToken, as_proxy_for=None)
    # fund user with sell Token
    tokenToSell.transfer(user1, sellAmount, {"from": token_whale})
    tokenToSell.approve(zap, sellAmount, {"from": user1})
    # start zapIn
    tx = zap.zapIn(
        sellToken,
        buyToken,
        curve_swap_address,
        sellAmount,
        swapTarget,
        vault,
        dataSwap,
        {"from": user1, "gas_price": gas_price, "amount": value},
    )
    # verify if sellToken balance
    assert tokenToSell.balanceOf(user1) == 0
    

    shares_balance = vault.balanceOf(user1)
    # verify if user received yearn shares
    assert shares_balance > 0
    assert (tx.events["ZapIn"]["tokensRec"] == shares_balance)
    # approve shares on yearn vault
    vault.approve(zap, shares_balance, {"from": user1})
    # configure 0x api for zapOut to AKRO
    parameters2 = {
        "sellToken": buyTokenName,
        "buyToken": sellToken,
        "sellAmount": 10000000000,
    }
    tokenToGetBalance = tokenToSell.balanceOf(user1)
    assert tokenToGetBalance == 0
    # params for zapOut
    request2 = requests.get(quote, params=parameters2)
    data2 = request2.json()
    sellToken1 = data2["sellTokenAddress"]
    buyToken1 = data2["buyTokenAddress"]
    swapTarget1 = data2["to"]
    dataSwap1 = data2["data"]
    # call zapOut
    tx = zap.zapOut(
        curve_swap_address,
        vault,
        shares_balance,
        swapTarget1,
        sellToken1,
        buyToken1,
        dataSwap1,
        {"from": user1},
    )
    # check if want balance is > 0
    assert tokenToSell.balanceOf(user1) > 0
    assert (tx.events["ZapOut"]["tokensRec"] == tokenToSell.balanceOf(user1))


# high value tokens
@parametrize_from_file(data, "data_zap_high")
def test_zap_low_liquidity(
    zap, user1, yearn_vault, sellTokenName, buyTokenName, whale, curve_address
):
    curve_swap_address = Contract.from_explorer(curve_address, as_proxy_for=None)
    vault = Contract.from_explorer(yearn_vault, as_proxy_for=None)
    token_whale = accounts.at(whale, force=True)
    parameters1 = {
        "buyToken": buyTokenName,
        "sellToken": sellTokenName,
        "sellAmount": 10000000000000,
    }
    request1 = requests.get(quote, params=parameters1)
    data1 = request1.json()
    sellToken = data1["sellTokenAddress"]
    buyToken = data1["buyTokenAddress"]
    sellAmount = data1["sellAmount"]
    buyAmount = data1["buyAmount"]
    swapTarget = data1["to"]
    dataSwap = data1["data"]
    gas_price = data1["gasPrice"]
    value = data1["value"]

    tokenToSell = Contract.from_explorer(sellToken, as_proxy_for=None)
    # fund user with sell Token
    tokenToSell.transfer(user1, sellAmount, {"from": token_whale})
    tokenToSell.approve(zap, sellAmount, {"from": user1})
    # start zapIn
    tx = zap.zapIn(
        sellToken,
        buyToken,
        curve_swap_address,
        sellAmount,
        swapTarget,
        vault,
        dataSwap,
        {"from": user1, "gas_price": gas_price, "amount": value},
    )
    # verify if sellToken balance
    assert tokenToSell.balanceOf(user1) == 0
    

    shares_balance = vault.balanceOf(user1)
    # verify if user received yearn shares
    assert shares_balance > 0
    assert (tx.events["ZapIn"]["tokensRec"] == shares_balance)
    # approve shares on yearn vault
    vault.approve(zap, shares_balance, {"from": user1})
    # configure 0x api for zapOut to AKRO
    parameters2 = {
        "sellToken": buyTokenName,
        "buyToken": sellToken,
        "sellAmount": buyAmount,
    }
    tokenToGetBalance = tokenToSell.balanceOf(user1)
    assert tokenToGetBalance == 0
    # params for zapOut
    request2 = requests.get(quote, params=parameters2)
    data2 = request2.json()
    sellToken1 = data2["sellTokenAddress"]
    buyToken1 = data2["buyTokenAddress"]
    swapTarget1 = data2["to"]
    dataSwap1 = data2["data"]
    # call zapOut
    tx = zap.zapOut(
        curve_swap_address,
        vault,
        shares_balance,
        swapTarget1,
        sellToken1,
        buyToken1,
        dataSwap1,
        {"from": user1},
    )
    # check if want balance is > 0
    assert tokenToSell.balanceOf(user1) > 0
    assert (tx.events["ZapOut"]["tokensRec"] == tokenToSell.balanceOf(user1))
