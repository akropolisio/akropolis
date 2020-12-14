import pytest
from brownie import accounts

@pytest.fixture(scope="module")
def deployer():
    yield accounts[0]

@pytest.fixture(scope="module")
def governance():
    yield accounts[0]

@pytest.fixture(scope="module")
def strategist():
    yield accounts[1]

@pytest.fixture
def rewards(accounts):
    yield accounts[2]

@pytest.fixture(scope="module")
def token(deployer, TestERC20):
    yield deployer.deploy(TestERC20, "Test Token", "TST", 18)

