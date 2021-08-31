import os
import pytest
from brownie import accounts
from brownie import Contract
import sys
from utils.deploy_helpers import deploy_proxy, deploy_admin

from dotenv import load_dotenv, find_dotenv


@pytest.fixture(scope="module")
def env_settings():
    yield load_dotenv(find_dotenv())

@pytest.fixture
def deployer():
    yield accounts[0]

@pytest.fixture
def dai(env_settings):
    dai_token = Contract.from_explorer(os.getenv("DAI"), as_proxy_for=None)
    yield dai_token


@pytest.fixture()
def crv(env_settings):
    crv_token = Contract.from_explorer(os.getenv("CRV"), as_proxy_for=None)
    yield crv_token


@pytest.fixture
def weth(env_settings):
    weth_address= Contract.from_explorer(os.getenv("WETH"), as_proxy_for=None)
    yield weth_address

@pytest.fixture(scope="module")
def user1():
    yield accounts[1]


@pytest.fixture(scope="module")
def user2():
    yield accounts[2]



@pytest.fixture
def zap(deployer, Zap, weth):
    zapContract = deployer.deploy(Zap, weth)
    yield zapContract

@pytest.fixture
def dai_owner():
    yield accounts.at("0x47ac0fb4f2d84898e4d9e7b4dab3c24507a6d503", force=True)


# @pytest.fixture
# def target():
#     abi=[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"stateMutability":"payable","type":"fallback"},{"inputs":[{"internalType":"bytes4","name":"selector","type":"bytes4"}],"name":"getFunctionImplementation","outputs":[{"internalType":"address","name":"impl","type":"address"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]
#     swapTarget = Contract.from_abi("ZeroEx", "0xDef1C0ded9bec7F1a1670819833240f027b25EfF", abi)
#     yield swapTarget


@pytest.fixture
def target():
    swapAddress = Contract("0xDef1C0ded9bec7F1a1670819833240f027b25EfF")
    yield swapAddress



