import pytest
from brownie import accounts
import sys

from utils.deploy_helpers import deploy_proxy, deploy_admin

TOTAL_TOKENS = 100000000000000


@pytest.fixture(scope="function", autouse=True)
def isolate_func(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass

@pytest.fixture(scope="module")
def deployer():
    yield accounts.add(
        "8fa2fdfb89003176a16b707fc860d0881da0d1d8248af210df12d37860996fb2"
    )


@pytest.fixture(scope="module")
def governance():
    yield accounts[1]


@pytest.fixture(scope="module")
def rewards(accounts):
    yield accounts[2]


@pytest.fixture(scope="module")
def strategist():
    yield accounts[3]


@pytest.fixture(scope="module")
def regular_user(accounts):
    yield accounts[0]


@pytest.fixture(scope="module")
def investment(accounts):
    yield accounts[4]


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
def vault(deployer, rewards, token, controller, TestVaultV2):
    vault = deployer.deploy(TestVaultV2)
    vault.initialize(token, deployer, rewards, "", "", {"from": deployer})
    vault.setGovernance(deployer, {"from": deployer})
    vault.setRewards(rewards, {"from": deployer})
    vault.setGuardian(deployer, {"from": deployer})
    vault.setDepositLimit(2 ** 256 - 1, {"from": deployer})
    vault.setManagementFee(0, {"from": deployer})

    yield vault


@pytest.fixture(scope="module")
def strategy(strategist, deployer, vault, token, investment, StubStrategyV2):
    strategy = strategist.deploy(StubStrategyV2, vault, investment, 200)
    token.approve(strategy, 10 ** 18, {"from": investment})
    strategy.setKeeper(strategist, {"from": strategist})

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


NULL_ADDRESS = "0x0000000000000000000000000000000000000000"


@pytest.fixture(scope="module")
def register_vault(
    deployer, token, vault, strategy, controller, registry, vaultSavings
):
    controller.setVault(token.address, vault.address, {"from": deployer})
    controller.approveStrategy(token.address, strategy.address, {"from": deployer})
    controller.setStrategy(token.address, strategy.address, {"from": deployer})

    assert registry.vaults(token.address, 0) == NULL_ADDRESS
    registry.newRelease(vault.address, {"from": deployer})
    assert registry.vaults(token.address, 0) == vault.address

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
