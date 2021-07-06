import pytest
from brownie import accounts
import sys

from utils.deploy_helpers import deploy_proxy, deploy_admin
from constantsV2 import *


@pytest.fixture(scope="module")
def deployer():
    yield accounts[0]


@pytest.fixture(scope="module")
def governance():
    yield accounts[0]


@pytest.fixture(scope="module")
def rewards(accounts):
    yield accounts[1]


@pytest.fixture(scope="module")
def strategist():
    yield accounts[2]


@pytest.fixture(scope="module")
def regular_user(accounts):
    yield accounts[3]


@pytest.fixture(scope="module")
def regular_user2(accounts):
    yield accounts[4]


@pytest.fixture(scope="module")
def investment(accounts):
    yield accounts[5]


@pytest.fixture(scope="module")
def investment2(accounts):
    yield accounts[6]


def prepare_token(deployer, regular_user, regular_user2, TestERC20):
    token = deployer.deploy(TestERC20, "Test Token", "TST", 18)
    token.mint(TOTAL_TOKENS, {"from": deployer})
    assert token.balanceOf(deployer) == TOTAL_TOKENS
    token.transfer(regular_user, TOTAL_TOKENS // 4, {"from": deployer})
    token.transfer(regular_user2, TOTAL_TOKENS // 4, {"from": deployer})

    return token


@pytest.fixture(scope="module")
def token(deployer, regular_user, regular_user2, TestERC20):
    token = prepare_token(deployer, regular_user, regular_user2, TestERC20)
    yield token


@pytest.fixture(scope="module")
def token2(deployer, regular_user, regular_user2, TestERC20):
    token = prepare_token(deployer, regular_user, regular_user2, TestERC20)
    yield token


def prepare_vault(deployer, rewards, token, TestVaultV2):
    vault = deployer.deploy(TestVaultV2)
    vault.initialize(token, deployer, rewards, "", "", {"from": deployer})
    vault.setGovernance(deployer, {"from": deployer})
    vault.setRewards(rewards, {"from": deployer})
    vault.setGuardian(deployer, {"from": deployer})
    vault.setDepositLimit(2 ** 256 - 1, {"from": deployer})
    vault.setManagementFee(0, {"from": deployer})

    return vault


@pytest.fixture(scope="module")
def vault(deployer, rewards, token, TestVaultV2):
    vault = prepare_vault(deployer, rewards, token, TestVaultV2)
    yield vault


@pytest.fixture(scope="module")
def vault2(deployer, rewards, token2, TestVaultV2):
    vault = prepare_vault(deployer, rewards, token2, TestVaultV2)
    yield vault


def prepare_strategy(strategist, deployer, vault, token, investment, StubStrategyV2):
    strategy = strategist.deploy(StubStrategyV2, vault, investment, STUB_YIELD)
    token.approve(strategy, 10 ** 18, {"from": investment})
    strategy.setKeeper(strategist, {"from": strategist})

    return strategy


@pytest.fixture(scope="module")
def strategy(strategist, deployer, vault, token, investment, StubStrategyV2):
    strategy = prepare_strategy(
        strategist, deployer, vault, token, investment, StubStrategyV2
    )

    yield strategy


@pytest.fixture(scope="function")
def strategy_vault2(strategist, deployer, vault2, token2, investment2, StubStrategyV2):
    strategy = prepare_strategy(
        strategist, deployer, vault2, token2, investment2, StubStrategyV2
    )

    yield strategy


@pytest.fixture(scope="module")
def strategy2(strategist, deployer, vault, token, investment2, StubStrategyV2):
    strategy = prepare_strategy(
        strategist, deployer, vault, token, investment2, StubStrategyV2
    )

    yield strategy


@pytest.fixture(scope="module")
def registry(deployer, TestRegistryV2):
    registry = deployer.deploy(TestRegistryV2)
    registry.setGovernance(deployer, {"from": deployer})
    yield registry


@pytest.fixture(scope="module")
def proxy_admin(deployer):
    proxy_admin = deploy_admin(deployer)
    yield proxy_admin


@pytest.fixture(scope="module")
def vaultSavings(deployer, proxy_admin, VaultSavingsV2):
    vaultSavingsImplFromProxy, vaultSavingsProxy, vaultSavingsImpl = deploy_proxy(
        deployer, proxy_admin, VaultSavingsV2
    )

    assert (
        vaultSavingsProxy.admin.call({"from": proxy_admin.address})
        == proxy_admin.address
    )
    assert (
        vaultSavingsProxy.implementation.call({"from": proxy_admin.address})
        == vaultSavingsImpl.address
    )

    yield vaultSavingsImplFromProxy


@pytest.fixture(scope="module")
def register_vault_in_system(deployer, governance, token, vault, strategy, registry):
    assert registry.vaults(token.address, 0) == NULL_ADDRESS
    registry.newRelease(vault.address, {"from": deployer})
    assert registry.vaults(token.address, 0) == vault.address

    vault.addStrategy(
        strategy,
        STRAT_DEBT_RATIO,
        STRAT_OPERATION_LIMIT,
        STRAT_OPERATION_FEE,
        {"from": governance},
    )


@pytest.fixture(scope="function")
def vault_add_second_strategy(deployer, governance, token, vault, strategy2, registry):
    vault.addStrategy(
        strategy2,
        STRAT_DEBT_RATIO,
        STRAT_OPERATION_LIMIT,
        STRAT_OPERATION_FEE,
        {"from": governance},
    )


@pytest.fixture(scope="function")
def register_vault2_in_system(
    deployer, governance, token2, vault2, strategy_vault2, registry
):
    registry.endorseVault(vault2.address, {"from": deployer})

    vault2.addStrategy(
        strategy_vault2,
        STRAT_DEBT_RATIO,
        STRAT_OPERATION_LIMIT,
        STRAT_OPERATION_FEE,
        {"from": governance},
    )


@pytest.fixture(scope="module")
def register_vault(register_vault_in_system, deployer, token, vault, vaultSavings):

    vaultSavings.registerVault(vault.address, {"from": deployer})
    assert vaultSavings.isVaultRegistered(vault.address) == True
    assert vaultSavings.isVaultActive(vault.address) == True
    assert vaultSavings.isBaseTokenForVault(vault.address, token.address) == True

    supported_vaults = vaultSavings.supportedVaults()
    assert len(supported_vaults) == 1
    assert supported_vaults[0] == vault.address

    active_vaults = vaultSavings.activeVaults()
    assert len(active_vaults) == 1
    assert active_vaults[0] == vault.address


@pytest.fixture(scope="function")
def register_vault2(register_vault2_in_system, deployer, vault2, vaultSavings):
    vaultSavings.registerVault(vault2.address, {"from": deployer})
