import pytest
from brownie import accounts

TOTAL_TOKENS = 10000000

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

@pytest.fixture
def investment(accounts):
    yield accounts[3]

@pytest.fixture(scope="module")
def token(deployer, TestERC20):
    token = deployer.deploy(TestERC20, "Test Token", "TST", 18)
    token.mint(TOTAL_TOKENS, {"from": deployer})
    assert token.balanceOf(deployer) == TOTAL_TOKENS
    yield token

