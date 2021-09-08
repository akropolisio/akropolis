import os
import pytest
from brownie import accounts
from brownie import Contract
import sys


from dotenv import load_dotenv, find_dotenv


@pytest.fixture(scope="module")
def env_settings():
    yield load_dotenv(find_dotenv())


@pytest.fixture
def deployer():
    yield accounts[0]


@pytest.fixture(scope="module")
def user1():
    yield accounts[1]


@pytest.fixture(scope="module")
def user2():
    yield accounts[2]


@pytest.fixture
def zap(deployer, Zap):
    registry = Contract.from_explorer(os.getenv("CURVEREG"), as_proxy_for=None)
    vaultSavings = Contract.from_explorer(
        os.getenv("VAULTSAVINGV2_PROXY"), as_proxy_for=os.getenv("VAULTSAVINGV2")
    )
    zapContract = deployer.deploy(Zap, registry, vaultSavings)
    yield zapContract


@pytest.fixture
def dai_owner():
    yield accounts.at("0x47ac0fb4f2d84898e4d9e7b4dab3c24507a6d503", force=True)
