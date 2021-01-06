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
def regular_user(accounts):
    yield accounts[1]

@pytest.fixture(scope="module")
def token(deployer, regular_user, TestERC20):
    token = deployer.deploy(TestERC20, "Test Token", "TST", 18)
    token.mint(TOTAL_TOKENS, {"from": deployer})
    assert token.balanceOf(deployer) == TOTAL_TOKENS
    token.transfer(regular_user, TOTAL_TOKENS // 2, {"from": deployer})
    yield token

@pytest.fixture(scope="module")
def controller(deployer, YTestController):
    controller = deployer.deploy(YTestController, deployer.address)
    yield controller

@pytest.fixture(scope="module")
def vault(deployer, token, controller, yTestVault):
    vault = deployer.deploy(yTestVault, token.address, controller.address)
    yield vault

@pytest.fixture(scope="module")
def strategy(deployer, token, YTestStrategy):
    strategy = deployer.deploy(YTestStrategy, token.address)
    yield strategy

@pytest.fixture(scope="module")
def registry(deployer, YTestRegistry):
    registry = deployer.deploy(YTestRegistry, deployer.address)
    yield registry

@pytest.fixture(scope="module")
def vaultSavings(deployer, VaultSavings):
    vaultSavings = deployer.deploy(VaultSavings)
    yield vaultSavings


    