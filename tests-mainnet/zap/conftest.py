import os
import pytest
from brownie import accounts
from brownie import Contract
import sys


from dotenv import load_dotenv, find_dotenv


@pytest.fixture(scope="module")
def env_settings():
    yield load_dotenv(find_dotenv())


@pytest.fixture(scope="function", autouse=True)
def deployer():
    accounts.default = accounts[0]
    yield accounts[0]


@pytest.fixture(scope="module")
def user1():
    yield accounts[1]


@pytest.fixture(scope="module")
def user2():
    yield accounts[2]


@pytest.fixture(scope="function", autouse=True)
def zap(deployer, Zap):
    registry = Contract.from_explorer(os.getenv("CURVEREG"), as_proxy_for=None)
    vaultSavings = Contract.from_explorer(
        os.getenv("VAULTSAVINGV2_PROXY"), as_proxy_for=os.getenv("VAULTSAVINGV2")
    )
    zapContract = deployer.deploy(Zap)
    zapContract.initialize(registry, vaultSavings, {"from": deployer})
    yield zapContract



@pytest.fixture
def target():
    a = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"stateMutability":"payable","type":"fallback"},{"inputs":[{"internalType":"bytes4","name":"selector","type":"bytes4"}],"name":"getFunctionImplementation","outputs":[{"internalType":"address","name":"impl","type":"address"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]
    ex = Contract.from_abi("ZeroEx", "0xDef1C0ded9bec7F1a1670819833240f027b25EfF", abi=a)
    yield ex

@pytest.fixture
def zapperData():
    contract = Contract.from_explorer("0xE03A338d5c305613AfC3877389DD3B0617233387", as_proxy_for=None)
    yield contract