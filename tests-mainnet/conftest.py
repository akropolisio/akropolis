import pytest
from brownie import accounts
from brownie import Contract, project
import sys
import os
import json

from utils.deploy_helpers import deploy_proxy, deploy_admin, upgrade_proxy, get_proxy_admin

from dotenv import load_dotenv, find_dotenv

ADEL_TO_SWAP = 100
AKRO_ON_SWAP = 10000
ADEL_AKRO_RATE = 15
EPOCH_LENGTH = 100
REWARDS_AMOUNT = 150

@pytest.fixture(scope="module")
def env_settings():
    yield load_dotenv(find_dotenv())

@pytest.fixture(scope="module")
def owner(env_settings, accounts):
    owner_addr = accounts.at(os.getenv("MAINNET_OWNER"), force=True)
    accounts[0].transfer(owner_addr, '80 ether')
    yield owner_addr

@pytest.fixture(scope="module")
def akro_staking_owner(env_settings, accounts):
    owner_addr = accounts.at(os.getenv("MAINNET_AKRO_STAKING_OWNER"), force=True)
    accounts[0].transfer(owner_addr, '10 ether')
    yield owner_addr

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
def akro(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_AKRO_PROXY"), as_proxy_for=os.getenv("MAINNET_AKRO"))


@pytest.fixture(scope="module")
def adel(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_ADEL_PROXY"), as_proxy_for=os.getenv("MAINNET_ADEL"))

@pytest.fixture(scope="module")
def vakro(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_VAKRO_PROXY"), as_proxy_for=os.getenv("MAINNET_VAKRO"))

@pytest.fixture(scope="module")
def adelstakingpool(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_ADEL_STAKING_PROXY"), as_proxy_for=os.getenv("MAINNET_ADEL_STAKING"))

@pytest.fixture(scope="module")
def akrostakingpool(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_AKRO_STAKING_PROXY"), as_proxy_for=os.getenv("MAINNET_AKRO_STAKING"))


@pytest.fixture(scope="module")
def vakroSwap(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("MAINNET_SWAP_PROXY"), as_proxy_for=os.getenv("MAINNET_SWAP"))

@pytest.fixture(scope="module")
def vakroSwapUpdated(env_settings, owner, vakroSwap, AdelVAkroSwap, Contract):
    proxy_admin = get_proxy_admin(os.getenv("MAINNET_PROXY_ADMIN"))

    mainnet_swap_new_impl =  Contract.from_explorer(os.getenv("MAINNET_SWAP_NEW"))

    proxy_admin.upgrade(vakroSwap, new_contract_impl.address, {'from': deployer})

    vakroSwapUpdated = Contract.from_abi(AdelVAkroSwap._name, vakroSwap.address, AdelVAkroSwap.abi)

    yield vakroSwapUpdated
