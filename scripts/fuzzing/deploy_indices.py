import os
from dotenv import load_dotenv, find_dotenv
from brownie import *
#IndicesSavings, HelperWETH, accounts, network, web3

from utils.deploy_helpers import deploy_proxy, deploy_admin, get_proxy_admin, upgrade_proxy
TOTAL_TOKENS = 1e30
NULL_ADDRESS = '0x0000000000000000000000000000000000000000'
ETH_ADDRESS = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

TOKEN_TOKEN1 = "token1"
TOKEN_TOKEN2 = "token2"
TOKEN_TOKEN3 = "token3"
TOKEN_INDEX1 = "index1"
TOKEN_INDEX2 = "index2"
TOKEN_INDEX3 = "index3"
TOKEN_WETH = "weth"

WETH_DECIMALS = 18

HARVEY_ORIGIN = '0xAaaaAaAAaaaAAaAAaAaaaaAAAAAaAaaaAaAaaAA0'
HARVEY_ACCOUNT_1 = '0xAaAaaAAAaAaaAaAaAaaAAaAaAAAAAaAAAaaAaAa2'
HARVEY_ACCOUNT_2 = '0xafFEaFFEAFfeAfFEAffeaFfEAfFEaffeafFeAFfE'

def amount_in_small_dimension(amount, token_instance):
    return int(10 ** token_instance.decimals() * amount)


def prepare_deployer():
    return accounts[0]
def governance():
    return accounts[0]
def rewards(accounts):
    return accounts[1]
def strategist():
    return accounts[2]
def prepare_regular_user(accounts):
    return HARVEY_ACCOUNT_1
def regular_user2(accounts):
    return HARVEY_ACCOUNT_2


def prepare_token(deployer, TestERC20, name, decimals):
    token = deployer.deploy(TestERC20, name, name, decimals)
    token.mint.transact(TOTAL_TOKENS * (10 ** decimals), {"from": deployer})
    return token
    
def prepare_weth(deployer, TestWETH):
    token = deployer.deploy(TestWETH)
    token.deposit({"from": deployer, "value": "50 ether"})
    return token
    
def prepare_tokens(deployer, TestERC20, TestWETH, weth):
    tokens = {}
    tokens[TOKEN_TOKEN1] = prepare_token(deployer, TestERC20, TOKEN_TOKEN1, 16)
    tokens[TOKEN_TOKEN2] = prepare_token(deployer, TestERC20, TOKEN_TOKEN2, 18)
    tokens[TOKEN_TOKEN3] = prepare_token(deployer, TestERC20, TOKEN_TOKEN3, 17)
    tokens[TOKEN_INDEX1] = prepare_token(deployer, TestERC20, TOKEN_INDEX1, 20)
    tokens[TOKEN_INDEX2] = prepare_token(deployer, TestERC20, TOKEN_INDEX2, 15)
    tokens[TOKEN_INDEX3] = prepare_token(deployer, TestERC20, TOKEN_INDEX3, 12)
    tokens[TOKEN_WETH] = weth
    return tokens

def prepare_uniswap_router(MockUniswapV2Router, deployer, TestERC20, tokens, weth):
    router = deployer.deploy(MockUniswapV2Router, weth.address)
    tokens[TOKEN_TOKEN1].transfer(router.address, amount_in_small_dimension(100, tokens[TOKEN_TOKEN1]), {"from": deployer})
    tokens[TOKEN_INDEX1].transfer(router.address, amount_in_small_dimension(100, tokens[TOKEN_INDEX1]), {"from": deployer})
    tokens[TOKEN_TOKEN2].transfer(router.address, amount_in_small_dimension(1000, tokens[TOKEN_TOKEN2]), {"from": deployer})
    tokens[TOKEN_INDEX2].transfer(router.address, amount_in_small_dimension(100000, tokens[TOKEN_INDEX2]), {"from": deployer})
    tokens[TOKEN_WETH].transfer(router.address, 10 * (10 **WETH_DECIMALS), {"from": deployer})

    router.mockAddLiquidity(tokens[TOKEN_TOKEN1].address, tokens[TOKEN_INDEX1].address, 1, 2, {"from": deployer})
    router.mockAddLiquidity(tokens[TOKEN_TOKEN1].address, tokens[TOKEN_WETH].address, 1000000, 2, {"from": deployer})
    router.mockAddLiquidity(tokens[TOKEN_INDEX1].address, tokens[TOKEN_WETH].address, 1000000, 1, {"from": deployer})

    router.mockAddLiquidity(tokens[TOKEN_TOKEN2].address, tokens[TOKEN_INDEX2].address, 1, 3, {"from": deployer})
    router.mockAddLiquidity(tokens[TOKEN_TOKEN2].address, tokens[TOKEN_WETH].address, 1000000, 3, {"from": deployer})
    router.mockAddLiquidity(tokens[TOKEN_INDEX2].address, tokens[TOKEN_WETH].address, 1000000, 1, {"from": deployer})

    router.addWrongPath(tokens[TOKEN_INDEX3].address)

    return router

def prepare_indices2(deployer, rewards, token2, TestIndices):
    indices = prepare_indices(deployer, rewards, token2, TestIndices)
    return indices
    
def prepare_helper_weth(deployer, HelperWETH):
    helper = deployer.deploy(HelperWETH)
    return helper

def proxy_admin(deployer):
    proxy_admin = deploy_admin(deployer)
    return proxy_admin

def prepare_indices_savings_swap(deployer, proxy_admin, IndicesSavings, tokens, uniswap_router, helper_weth):
    indicesSavingsImplFromProxy, indicesSavingsProxy, indicesSavingsImpl = deploy_proxy(deployer, proxy_admin, IndicesSavings, helper_weth.address)
    assert indicesSavingsProxy.admin.call({"from":proxy_admin.address}) == proxy_admin.address
    assert indicesSavingsProxy.implementation.call({"from":proxy_admin.address}) == indicesSavingsImpl.address

    indicesSavingsImplFromProxy.registerIndex(tokens[TOKEN_INDEX1], uniswap_router.address, {'from': deployer})
    indicesSavingsImplFromProxy.registerIndex(tokens[TOKEN_INDEX3], uniswap_router.address, {'from': deployer})

    return indicesSavingsImplFromProxy

def main():
    deployer = prepare_deployer()
    regular_user = prepare_regular_user(accounts)

    weth = prepare_weth(deployer, TestWETH)
    tokens = prepare_tokens(deployer, TestERC20, TestWETH, weth)
    uniswap_router = prepare_uniswap_router(MockUniswapV2Router, deployer, TestERC20, tokens, weth)
    helper_weth = prepare_helper_weth(deployer, HelperWETH)

    indices_savings_swap = prepare_indices_savings_swap(deployer, proxy_admin(deployer), IndicesSavings, tokens, uniswap_router, helper_weth)

#     buy_amount=1422151
#     buy_amount_out_min=11
#     sell_amount=15
#     sell_amount_out_min=2
#
#     tokens[TOKEN_TOKEN1].transfer(regular_user, buy_amount, {'from': deployer})
#     tokens[TOKEN_TOKEN1].approve(indices_savings_swap.address, buy_amount, {'from': regular_user})
#     path = [tokens[TOKEN_TOKEN1].address, tokens[TOKEN_INDEX1].address]
#     indices_savings_swap.buy['address,address,uint,uint,address[]'](
#         tokens[TOKEN_INDEX1].address,
#         tokens[TOKEN_TOKEN1].address,
#         buy_amount,
#         buy_amount_out_min,
#         path,
#         {'from': regular_user}
#         )
#
#     tokens[TOKEN_INDEX1].transfer(regular_user, sell_amount, {'from': deployer})
#     tokens[TOKEN_INDEX1].approve(indices_savings_swap.address, sell_amount, {'from': regular_user})
#     path = [tokens[TOKEN_INDEX1].address, tokens[TOKEN_TOKEN1].address]
#     indices_savings_swap.sell['address,address,uint,uint,address[]'](
#         tokens[TOKEN_INDEX1].address,
#         tokens[TOKEN_TOKEN1].address,
#         sell_amount,
#         sell_amount_out_min,
#         path,
#         {'from': regular_user}
#         )

