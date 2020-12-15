import pytest
from brownie import accounts

TOTAL_TOKENS = 10000000
STRAT_CREDIT = TOTAL_TOKENS // 2
STRAT_OPERATION_LIMIT = TOTAL_TOKENS // 4
STRAT_OPERATION_FEE = 10

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
def strategy(strategist, deployer, vault, token, investment, StubStrategy):
    strategy = strategist.deploy(StubStrategy, vault, investment, 10)
    token.approve(strategy, 10**18, {"from":investment})
    strategy.setKeeper(strategist, {"from": strategist})

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

def test_vault_setup_strategy(chain, vault, strategy, token, investment, deployer, strategist, governance):
    vault.addStrategy(strategy, STRAT_CREDIT, STRAT_OPERATION_LIMIT, STRAT_OPERATION_FEE, {"from": governance})

    assert vault.creditAvailable(strategy) == 0
    assert vault.debtOutstanding(strategy) == 0

    assert vault.balanceSheetOfStrategy(strategy) == 0
    assert strategy.estimatedTotalAssets() == 0

    #deposit to vault
    deposited_tokens = token.balanceOf(deployer) // 2
    token.approve(vault, deposited_tokens, {"from": deployer})
    vault.deposit(deposited_tokens, {"from": deployer})

    assert token.balanceOf(vault) == deposited_tokens
    assert vault.totalDebt() == 0  # No connected strategies yet
    assert vault.balanceOf(deployer) == deposited_tokens

    #deposit to strategy
    start = chain.time()
    chain.mine(1, start + 1)
    strategy.harvest({"from": strategist})
    
    #Funds are invested
    assert token.balanceOf(investment) == STRAT_CREDIT + STRAT_OPERATION_FEE
    assert vault.debtOutstanding(strategy, {"from": strategy}) == 0


def test_yield():
    pass

def test_withdraw(token, vault, strategy):
    pass

