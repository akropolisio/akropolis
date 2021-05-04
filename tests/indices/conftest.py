import pytest
from brownie import accounts
import sys

from utils.deploy_helpers import deploy_proxy, deploy_admin
from constants import *
from utils.utils import amount_in_small_dimension

@pytest.fixture(scope="module")
def deployer():
    yield accounts[0]


@pytest.fixture(scope="module")
def governance():
    yield accounts[0]


@pytest.fixture(scope="module")
def rewards(accounts):
    yield accounts[1]


@pytest.fixture(scope="module")
def strategist():
    yield accounts[2]


@pytest.fixture(scope="module")
def regular_user(accounts):
    yield accounts[3]

@pytest.fixture(scope="module")
def regular_user2(accounts):
    yield accounts[4]


@pytest.fixture(scope="module")
def investment(accounts):
    yield accounts[5]


@pytest.fixture(scope="module")
def investment2(accounts):
    yield accounts[6]


def prepare_token(deployer, TestERC20, name, decimals):
    token = deployer.deploy(TestERC20, name, name, decimals)
    token.mint(TOTAL_TOKENS * (10 ** decimals), {"from": deployer})
    return token


@pytest.fixture(scope="module")
def weth(deployer, TestWETH):
    token = deployer.deploy(TestWETH)
    token.deposit({"from": deployer, "value": "50 ether"})
    yield token


@pytest.fixture(scope="module")
def tokens(deployer, TestERC20, TestWETH, weth):
    tokens = {}
    tokens[TOKEN_TOKEN1] = prepare_token(deployer, TestERC20, TOKEN_TOKEN1, 16)
    tokens[TOKEN_TOKEN2] = prepare_token(deployer, TestERC20, TOKEN_TOKEN2, 18)
    tokens[TOKEN_TOKEN3] = prepare_token(deployer, TestERC20, TOKEN_TOKEN3, 17)
    tokens[TOKEN_INDEX1] = prepare_token(deployer, TestERC20, TOKEN_INDEX1, 20)
    tokens[TOKEN_INDEX2] = prepare_token(deployer, TestERC20, TOKEN_INDEX2, 15)
    tokens[TOKEN_INDEX3] = prepare_token(deployer, TestERC20, TOKEN_INDEX3, 12)
    tokens[TOKEN_WETH] = weth
    yield tokens


@pytest.fixture(scope="module")
def uniswap_router(MockUniswapV2Router, deployer, TestERC20, tokens, weth):
    router = deployer.deploy(MockUniswapV2Router, weth.address)
    tokens[TOKEN_TOKEN1].transfer(router.address, amount_in_small_dimension(100, tokens[TOKEN_TOKEN1]), {"from": deployer})
    tokens[TOKEN_INDEX1].transfer(router.address, amount_in_small_dimension(100, tokens[TOKEN_INDEX1]), {"from": deployer})
    tokens[TOKEN_WETH].transfer(router.address, 10 * (10 ** WETH_DECIMALS), {"from": deployer})

    router.mockAddLiquidity(tokens[TOKEN_TOKEN1].address, tokens[TOKEN_INDEX1].address, 1, 2, {"from": deployer})
    router.mockAddLiquidity(tokens[TOKEN_TOKEN1].address, tokens[TOKEN_WETH].address, 1000000, 2, {"from": deployer})
    router.mockAddLiquidity(tokens[TOKEN_INDEX1].address, tokens[TOKEN_WETH].address, 1000000, 1, {"from": deployer})

    router.addWrongPath(tokens[TOKEN_TOKEN3].address)

    yield router


@pytest.fixture(scope="module")
def uniswap_router2(MockUniswapV2Router, deployer, TestERC20, tokens, weth):
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

    yield router


@pytest.fixture(scope="module")
def indices2(deployer, rewards, token2, TestIndices):
    indices = prepare_indices(deployer, rewards, token2, TestIndices)
    yield indices


@pytest.fixture(scope="module")
def helper_weth(deployer, HelperWETH):
    helper = deployer.deploy(HelperWETH)
    yield helper


@pytest.fixture(scope="module")
def proxy_admin(deployer):
    proxy_admin = deploy_admin(deployer)
    yield proxy_admin

@pytest.fixture(scope="module")
def indices_savings_basic(deployer, proxy_admin, IndicesSavings, helper_weth):
    indicesSavingsImplFromProxy, indicesSavingsProxy, indicesSavingsImpl = deploy_proxy(deployer, proxy_admin, IndicesSavings, helper_weth.address)
    assert indicesSavingsProxy.admin.call({"from":proxy_admin.address}) == proxy_admin.address
    assert indicesSavingsProxy.implementation.call({"from":proxy_admin.address}) == indicesSavingsImpl.address
    yield indicesSavingsImplFromProxy


@pytest.fixture(scope="module")
def indices_savings_swap(deployer, proxy_admin, IndicesSavings, tokens, uniswap_router, uniswap_router2, helper_weth):
    indicesSavingsImplFromProxy, indicesSavingsProxy, indicesSavingsImpl = deploy_proxy(deployer, proxy_admin, IndicesSavings, helper_weth.address)
    assert indicesSavingsProxy.admin.call({"from":proxy_admin.address}) == proxy_admin.address
    assert indicesSavingsProxy.implementation.call({"from":proxy_admin.address}) == indicesSavingsImpl.address

    indicesSavingsImplFromProxy.registerIndex(tokens[TOKEN_INDEX1], uniswap_router.address, {'from': deployer})
    indicesSavingsImplFromProxy.registerIndex(tokens[TOKEN_INDEX2], uniswap_router2.address, {'from': deployer})
    indicesSavingsImplFromProxy.registerIndex(tokens[TOKEN_INDEX3], uniswap_router.address, {'from': deployer})

    yield indicesSavingsImplFromProxy
