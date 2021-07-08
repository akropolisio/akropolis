import pytest
from brownie import accounts
import sys

from utils.deploy_helpers import deploy_proxy, deploy_admin


@pytest.fixture(scope="module")
def deployer():
    yield accounts[0]


@pytest.fixture(scope="module")
def regular_user(accounts):
    yield accounts[1]


@pytest.fixture(scope="module")
def regular_user2(accounts):
    yield accounts[2]


@pytest.fixture(scope="module")
def regular_user3(accounts):
    yield accounts[3]


@pytest.fixture(scope="module")
def regular_user4(accounts):
    yield accounts[4]


@pytest.fixture(scope="module")
def proxy_admin(deployer):
    proxy_admin = deploy_admin(deployer)
    yield proxy_admin


@pytest.fixture(scope="function")
def token(deployer, TestERC20):
    token = deployer.deploy(TestERC20, "token", "TKN", 18)
    token.mint(1500000000, {"from": deployer})
    return token


@pytest.fixture(scope="function")
def rewards(deployer, proxy_admin, token, Rewards):
    rewardsImplFromProxy, rewardsProxy, rewardsImpl = deploy_proxy(
        deployer, proxy_admin, Rewards, token.address
    )

    assert rewardsProxy.admin.call({"from": proxy_admin.address}) == proxy_admin.address
    assert (
        rewardsProxy.implementation.call({"from": proxy_admin.address})
        == rewardsImpl.address
    )

    yield rewardsImplFromProxy
