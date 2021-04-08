import pytest
from brownie import accounts
from brownie import Contract, project
import sys
import os
import json

from utils.deploy_helpers import deploy_proxy, deploy_admin, upgrade_proxy, get_proxy_admin
from constants import *
from dotenv import load_dotenv, find_dotenv
from utils.utils import amount_in_small_dimension

ADEL_TO_SWAP = 100
AKRO_ON_SWAP = 10000
ADEL_AKRO_RATE = 15
EPOCH_LENGTH = 100
REWARDS_AMOUNT = 150

@pytest.fixture(scope="module")
def env_settings():
    yield load_dotenv(find_dotenv())

@pytest.fixture(scope="module")
def deployer(env_settings, accounts):
    yield accounts[0]

@pytest.fixture(scope="module")
def regular_user(accounts):
    yield accounts[1]

@pytest.fixture(scope="module")
def exchange_pool(accounts):
    yield accounts[2]

@pytest.fixture(scope="module")
def sushi_router(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_SUSHI_ROUTER"))

@pytest.fixture(scope="module")
def pipt(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_PIPT"))

@pytest.fixture(scope="module")
def yeti(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_YETI"))

@pytest.fixture(scope="module")
def assy(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_ASSY"))

@pytest.fixture(scope="module")
def yla(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_YLA"))

@pytest.fixture(scope="module")
def usdt(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_USDT"))

@pytest.fixture(scope="module")
def usdc(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_USDC"))

@pytest.fixture(scope="module")
def tokens(deployer,sushi_router,usdc,usdt,pipt,yeti,assy,yla):
    tokens = {}
    tokens[TOKEN_USDT] = usdt
    tokens[TOKEN_USDC] = usdc
    tokens[TOKEN_PIPT] = pipt
    tokens[TOKEN_YETI] = yeti
    tokens[TOKEN_ASSY] = assy
    tokens[TOKEN_YLA] = yla
    tokens[TOKEN_WETH] = Contract.from_explorer(sushi_router.WETH())
    yield tokens

@pytest.fixture(scope="module")
def paths(tokens):
    path_for_tokens = [TOKEN_USDT, TOKEN_USDC, TOKEN_PIPT, TOKEN_YETI, TOKEN_ASSY, TOKEN_YLA]
    paths = {}
    for id in path_for_tokens:
        paths[id] = [tokens[TOKEN_WETH].address, tokens[id].address]
    paths[TOKEN_YLA] = [tokens[TOKEN_WETH].address, tokens[TOKEN_USDC].address, tokens[TOKEN_YLA].address]
    yield paths

@pytest.fixture(scope="module")
def get_tokens(deployer,sushi_router,exchange_pool,tokens,paths):
    mint_tokens = [TOKEN_USDT, TOKEN_USDC, TOKEN_PIPT, TOKEN_YETI, TOKEN_ASSY, TOKEN_YLA]
    for id in mint_tokens:
        sushi_router.swapExactETHForTokens(
            amount_in_small_dimension(100, tokens[id]),
            paths[id],
            deployer,
            1893456000, # 1 January 2030
            {"from": exchange_pool, "value": "5 ether"}
            )
        assert tokens[id].balanceOf(deployer) > 0

    yield tokens

@pytest.fixture(scope="module")
def helper_weth(deployer, HelperWETH):
    helper = deployer.deploy(HelperWETH)
    yield helper

@pytest.fixture(scope="module")
def proxy_admin(deployer):
    proxy_admin = deploy_admin(deployer)
    yield proxy_admin

@pytest.fixture(scope="module")
def indices_savings_swap(get_tokens, deployer, proxy_admin, IndicesSavings, sushi_router, tokens, helper_weth):
    indicesSavingsImplFromProxy, indicesSavingsProxy, indicesSavingsImpl = deploy_proxy(deployer, proxy_admin, IndicesSavings, helper_weth.address)
    assert indicesSavingsProxy.admin.call({"from":proxy_admin.address}) == proxy_admin.address
    assert indicesSavingsProxy.implementation.call({"from":proxy_admin.address}) == indicesSavingsImpl.address

    indicesSavingsImplFromProxy.registerIndex(tokens[TOKEN_PIPT], sushi_router.address, {'from': deployer})
    indicesSavingsImplFromProxy.registerIndex(tokens[TOKEN_YETI], sushi_router.address, {'from': deployer})
    indicesSavingsImplFromProxy.registerIndex(tokens[TOKEN_ASSY], sushi_router.address, {'from': deployer})
    indicesSavingsImplFromProxy.registerIndex(tokens[TOKEN_YLA], sushi_router.address, {'from': deployer})

    yield indicesSavingsImplFromProxy
