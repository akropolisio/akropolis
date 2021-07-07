import pytest
from brownie import accounts
from brownie import Contract, project
import sys
import os
import json

from utils.deploy_helpers import (
    deploy_proxy,
    deploy_admin,
    upgrade_proxy,
    get_proxy_admin,
)

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
    accounts[0].transfer(owner_addr, "80 ether")
    yield owner_addr


@pytest.fixture(scope="module")
def akro_staking_owner(env_settings, accounts):
    owner_addr = accounts.at(os.getenv("MAINNET_AKRO_STAKING_OWNER"), force=True)
    accounts[0].transfer(owner_addr, "10 ether")
    yield owner_addr


@pytest.fixture(scope="module")
def proxy_admin(env_settings, accounts):
    yield os.getenv("MAINNET_PROXY_ADMIN")


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
def akro(Contract, env_settings):
    yield Contract.from_explorer("0x8ab7404063ec4dbcfd4598215992dc3f8ec853d7", as_proxy_for="0xEaA04Ea9a674d755B9c2fD988d01F7A1C9D116dA")


@pytest.fixture(scope="module")
def akroowner(env_settings):
    yield os.getenv("MAINNET_AKRO_OWNER")


@pytest.fixture(scope="module")
def adel(Contract, env_settings):
    yield Contract.from_explorer(
        os.getenv("MAINNET_ADEL_PROXY"), as_proxy_for=os.getenv("MAINNET_ADEL")
    )


@pytest.fixture(scope="module")
def vakro(Contract, env_settings):
    yield Contract.from_explorer(
        os.getenv("MAINNET_VAKRO_PROXY"), as_proxy_for=os.getenv("MAINNET_VAKRO")
    )


@pytest.fixture(scope="module")
def adelstakingpool(Contract, env_settings):
    yield Contract.from_explorer(
        os.getenv("MAINNET_ADEL_STAKING_PROXY"),
        as_proxy_for=os.getenv("MAINNET_ADEL_STAKING"),
    )


@pytest.fixture(scope="module")
def akrostakingpool(Contract, env_settings):
    yield Contract.from_explorer(
        os.getenv("MAINNET_AKRO_STAKING_PROXY"),
        as_proxy_for=os.getenv("MAINNET_AKRO_STAKING"),
    )


@pytest.fixture(scope="module")
def vakroSwap(Contract, env_settings):
    yield Contract.from_explorer(
        os.getenv("MAINNET_SWAP_PROXY"), as_proxy_for=os.getenv("MAINNET_SWAP")
    )


@pytest.fixture(scope="module")
def vakroVestingSwap(
    env_settings, owner, proxy_admin, AdelVAkroVestingSwap, akro, adel, vakro
):
    (
        vakroVestingSwapImplFromProxy,
        vakroVestingSwapProxy,
        vakroVestingSwapImpl,
    ) = deploy_proxy(
        owner,
        proxy_admin,
        AdelVAkroVestingSwap,
        akro.address,
        adel.address,
        vakro.address,
    )
    yield vakroVestingSwapImplFromProxy
