import pytest
from brownie import accounts

def test_prepare_token(token, deployer):
    token.mint(10000000, {"from": deployer})
    assert token.balanceOf(deployer) == 10000000

@pytest.fixture
def vault(deployer, token, rewards, Vault):
    vault = deployer.deploy(Vault, token, deployer, rewards, "", "")
    vault.setGovernance(deployer, {"from": deployer})
    vault.setRewards(rewards, {"from": deployer})
    vault.setGuardian(deployer, {"from": deployer})

    assert token.balanceOf(vault) == 0
    assert vault.totalDebt() == 0  # No connected strategies yet
    yield vault

@pytest.fixture
def strategy(strategist, deployer, vault, token, StubStrategy):
    strategy = strategist.deploy(StubStrategy, vault)
    # Addresses
    assert strategy.strategist() == strategist
    assert strategy.rewards() == strategist
    assert strategy.keeper() == strategist
    assert strategy.want() == vault.token()
    assert strategy.name() == "StubCurveStrategy"

    assert not strategy.emergencyExit()

    # Should not trigger until it is approved
    assert not strategy.harvestTrigger(0)
    assert not strategy.tendTrigger(0)
    yield strategy

def test_vault_setup_strategy(vault, strategy, governance):
    vault.addStrategy(strategy, 0, 0, 0, {"from": governance})

    assert vault.creditAvailable(strategy) == 0
    assert vault.debtOutstanding(strategy) == 0

def test_initial_balance(vault, strategy):
    assert vault.balanceSheetOfStrategy(strategy) == 0
    assert strategy.estimatedTotalAssets() == 0

def test_deposit_to_vault(vault, token, deployer):
    token.approve(vault, token.balanceOf(deployer) // 2, {"from": deployer})
    vault.deposit(token.balanceOf(deployer) // 2, {"from": deployer})

    assert token.balanceOf(vault) != 0
    assert token.balanceOf(vault) == token.balanceOf(deployer)
    assert vault.totalDebt() == 0  # No connected strategies yet


def test_deposit_to_strategy():
    pass

def test_yield():
    pass

def test_withdraw(token, vault, strategy):
    pass

