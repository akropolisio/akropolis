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
def rewards(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("REWARDS"))


@pytest.fixture(scope="module")
def voters(env_settings, Contract):
    yield Contract.from_explorer(os.getenv("VOTER_PROXY"), as_proxy_for=None)


@pytest.fixture(scope="module")
def strategist(env_settings):
    yield accounts.at(os.getenv("STRATEGIST"), force=True)
