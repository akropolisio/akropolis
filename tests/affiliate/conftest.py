import pytest
from brownie import accounts
import sys
from constantsV2 import *
from utils.deploy_helpers import deploy_proxy, deploy_admin

@pytest.fixture(scope="function")
def deployer():
    yield accounts[0]

@pytest.fixture(scope="function")
def gov():
    yield accounts[7]

@pytest.fixture(scope="function")
def affiliate():
    yield accounts[0] 

@pytest.fixture(scope="function")
def rewards(accounts):
    yield accounts[1]

@pytest.fixture(scope="function")
def strategist():
    yield accounts[2]

@pytest.fixture(scope="function")
def regular_user(accounts):
    yield accounts[3]

@pytest.fixture(scope="function")
def regular_user2(accounts):
    yield accounts[4]

@pytest.fixture(scope="function")
def investment(accounts):
    yield accounts[5]

@pytest.fixture(scope="function")
def investment2(accounts):
    yield accounts[6]

@pytest.fixture
def rando(accounts):
    yield accounts[9]


def prepare_token(deployer, gov, TestERC20):
    token = deployer.deploy(TestERC20, "Test Token", "TST", 18)
    token.mint(TOTAL_TOKENS, {"from": deployer})
    assert token.balanceOf(deployer) == TOTAL_TOKENS
    token.transfer(gov, TOTAL_TOKENS, {"from": deployer})

    return token

@pytest.fixture(scope="function")
def token(deployer, gov, TestERC20):
    token = prepare_token(deployer, gov, TestERC20)
    yield token

@pytest.fixture(scope="function")
def token2(deployer, regular_user, regular_user2, TestERC20):
    token = prepare_token(deployer, regular_user, regular_user2, TestERC20)
    yield token

def prepare_vault(deployer, gov, rewards, token, TestVaultV2):
    vault = deployer.deploy(TestVaultV2)
    vault.initialize(token, deployer, rewards, "", "", {"from": deployer})
    vault.setGovernance(gov, {"from": deployer})
    vault.acceptGovernance({"from": gov})
    vault.setRewards(rewards, {"from": gov})
    vault.setGuardian(deployer, {"from": gov})
    vault.setDepositLimit(2 ** 256 - 1, {"from": gov})
    vault.setManagementFee(0, {"from": gov})

    return vault

@pytest.fixture(scope="function")
def vault(deployer, gov, rewards, token, TestVaultV2):
    vault = prepare_vault(deployer, gov, rewards, token, TestVaultV2)
    yield vault

@pytest.fixture(scope="function")
def vault2(deployer, gov, rewards, token2, TestVaultV2):
    vault = prepare_vault(deployer, gov, rewards, token2, TestVaultV2)
    yield vault


def prepare_strategy(strategist, deployer, vault, token, investment, StubStrategyV2):
    strategy = strategist.deploy(StubStrategyV2, vault, investment, STUB_YIELD)
    token.approve(strategy, 10**18, {"from":investment})
    strategy.setKeeper(strategist, {"from": strategist})

    return strategy

@pytest.fixture(scope="function")
def strategy(strategist, deployer, vault, token, investment, StubStrategyV2):
    strategy = prepare_strategy(strategist, deployer, vault, token, investment, StubStrategyV2)

    yield strategy


@pytest.fixture(scope="function")
def strategy_vault2(strategist, deployer, vault2, token2, investment2, StubStrategyV2):
    strategy = prepare_strategy(strategist, deployer, vault2, token2, investment2, StubStrategyV2)

    yield strategy

@pytest.fixture(scope="function")
def strategy2(strategist, deployer, vault, token, investment2, StubStrategyV2):
    strategy = prepare_strategy(strategist, deployer, vault, token, investment2, StubStrategyV2)

    yield strategy

@pytest.fixture(scope="function")
def registry(deployer, gov, TestRegistryV2):
    registry = deployer.deploy(TestRegistryV2)
    registry.setGovernance(gov,  {"from": deployer})
    registry.acceptGovernance({"from": gov})
    assert registry.governance() == gov
    yield registry

@pytest.fixture(scope="function")
def proxy_admin(deployer):
    proxy_admin = deploy_admin(deployer)
    yield proxy_admin

@pytest.fixture(scope="function")
def affiliate_token(token, affiliate, registry, AffiliateToken):
    # Affliate Wrapper
    yield affiliate.deploy(
        AffiliateToken,
        token,
        registry,
        f"Affiliate {token.symbol()}",
        f"af{token.symbol()}",
    )


@pytest.fixture(scope="function")
def register_vault_in_system(deployer, gov, token, vault, strategy, registry):
    assert registry.vaults(token.address, 0) == NULL_ADDRESS
    registry.newRelease(vault.address, {'from': deployer})
    assert registry.vaults(token.address, 0) == vault.address
    
    vault.addStrategy(strategy, STRAT_DEBT_RATIO, STRAT_OPERATION_LIMIT, STRAT_OPERATION_FEE, {"from": gov})

@pytest.fixture(scope="function")
def vault_add_second_strategy(deployer, gov, token, vault, strategy2, registry):    
    vault.addStrategy(strategy2, STRAT_DEBT_RATIO, STRAT_OPERATION_LIMIT, STRAT_OPERATION_FEE, {"from": gov})

@pytest.fixture(scope="function")
def register_vault2_in_system(deployer, gov, token2, vault2, strategy_vault2, registry):
    registry.endorseVault(vault2.address, {'from': deployer})
    
    vault2.addStrategy(strategy_vault2, STRAT_DEBT_RATIO, STRAT_OPERATION_LIMIT, STRAT_OPERATION_FEE, {"from": gov})




