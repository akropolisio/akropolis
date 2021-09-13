import pytest
import brownie
import time
from brownie import accounts, chain
import requests, json
from brownie import Contract
import parametrize_from_file

quote = f"https://api.0x.org/swap/v1/quote"


data = "./data/data.json"
amount = 100e18


@parametrize_from_file(data, "data_zap_high")
def test_zap_high_liquidity(
    zap, user1, yearn_vault, sellTokenName, buyTokenName, whale, curve_address, vault_owner, amount_in, deployer
):
    curve_swap_address = Contract.from_explorer(curve_address, as_proxy_for=None)
    vault = Contract.from_explorer(yearn_vault, as_proxy_for=None)
    
    token_whale = accounts.at(whale, force=True)
    parameters1 = {
        "buyToken": buyTokenName,
        "sellToken": sellTokenName,
        "sellAmount": amount_in,
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

    zap.setApprovedTokens([sellToken], [True], {"from": deployer})

    chain.mine(100)

    tokenToSell = Contract.from_explorer(sellToken, as_proxy_for=None)
    # fund user with sell Token
    tokenToSell.transfer(user1, sellAmount, {"from": token_whale})
    tokenToSell.approve(zap, sellAmount, {"from": user1})
    min_amount = curve_swap_address.calc_token_amount([int(buyAmount), 0, 0], True)

    print(min_amount)

    #test slippage 3%
    slippage = 0.3 * min_amount
    amount_min = min_amount - slippage
    #add the token to approve array

    # start zapIn
    tx = zap.zapIn(
        sellToken,
        buyToken,
        curve_swap_address,
        sellAmount,
        amount_min,
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



@parametrize_from_file(data, "data_zap_high")
def test_zap_out(zap, user1, yearn_vault, sellTokenName, buyTokenName, vault_owner, curve_address, whale, zapperData, amount_in):
    vault = Contract.from_explorer(yearn_vault, as_proxy_for=None)
    curve_swap_address = Contract.from_explorer(curve_address, as_proxy_for=None)
    account_owner = accounts.at(vault_owner, force=True)
    vault.transfer(user1, amount, {"from": account_owner})
    vault.approve(zap, amount, {"from": user1})
    parameters = {
        "sellToken": buyTokenName,
        "buyToken": sellTokenName,
        "sellAmount": 100000000
    }
    request = requests.get(quote, params=parameters)
    data = request.json()
    sellToken = data["sellTokenAddress"]
    buyToken = data["buyTokenAddress"]
    dataSwap = data["data"]
    swapTarget = data["to"]

    wantedToken= Contract.from_explorer(buyToken, as_proxy_for=None)
    assert wantedToken.balanceOf(user1) == 0
    # min_amount = zapperData.removeLiquidityReturn(curve_swap_address, sellToken, )
    tx = zap.zapOut(
        curve_swap_address,
        vault,
        amount,
        0,
        swapTarget,
        sellToken,
        buyToken,
        dataSwap,
        {"from": user1},
    )
    

    assert(tx.events["ZapOut"]["tokensRec"] ==  wantedToken.balanceOf(user1))






