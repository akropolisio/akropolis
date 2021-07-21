import pytest
from brownie import Contract, project
from brownie import accounts
import sys
import os
import json


from dotenv import load_dotenv, find_dotenv


@pytest.fixture(scope="module")
def env_settings():
    yield load_dotenv(find_dotenv())


def prepare_strategy(strategist, deployer, vault, token, investment, StubStrategyV2):
    strategy = strategist.deploy(StubStrategyV2, vault, investment, STUB_YIELD)
    token.approve(strategy, 10 ** 18, {"from": investment})
    strategy.setKeeper(strategist, {"from": strategist})

    return strategy


@pytest.fixture(scope="module")
def strategy(strategist, deployer, vault, token, investment, StubStrategyV2):
    strategy = prepare_strategy(
        strategist, deployer, vault, token, investment, StubStrategyV2
    )

    yield strategy

@pytest.fixture(scope="module")
def owner(env_settings):
    yield accounts.at(os.getenv("PROXY_OWNER"), force=True)


@pytest.fixture(scope="module")
def regular_user(accounts):
    yield accounts[1]


@pytest.fixture(scope="module")
def regular_user1(accounts):
    yield accounts[2]


@pytest.fixture(scope="module")
def vault_savings(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("VAULTSAVINGV2_PROXY"), as_proxy_for=os.getenv("VAULTSAVINGV2"))


@pytest.fixture(scope="module")
def vault_tricrypto(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("TRYCRYPTO"), as_proxy_for=None)


@pytest.fixture(scope="module")
def governance(env_settings):
    yield accounts.at(os.getenv("GOVERNANCE"), force=True)


@pytest.fixture(scope="module")
def lpToken(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("LPTOKEN"), as_proxy_for=None)


@pytest.fixture(scope="module")
def lptoken_owner(env_settings):
    yield accounts.at(os.getenv("LPTOKEN_OWNER"), force=True)


@pytest.fixture(scope="module")
def rewards(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("REWARDS"))


