import pytest
from brownie import accounts

TOTAL_TOKENS = 10000000
STUB_YIELD = 200
STRAT_DEBT_RATIO = 5000 # 10000 is MAX
STRAT_OPERATION_LIMIT = TOTAL_TOKENS // 4
DEPOSIT_VALUE = TOTAL_TOKENS // 4
WITHDRAW_VALUE = DEPOSIT_VALUE // 2
STRAT_OPERATION_FEE = 100 # 1% of yield (per Strategy) - default
PERFORMANCE_FEE = 1000  # 10% of yield (per Strategy) - default
MANAGEMENT_FEE = 200  # 2% per year - default
CONST_VAULT_MAX_BPS = 10000 # MAX_BPS

def calc_shares(token, vault, amount):
    return int( (token.balanceOf(vault) + vault.totalDebt()) * amount / float(vault.totalSupply()) )

@pytest.fixture
def vault(deployer, token, rewards, TestVaultV2):
    vault = deployer.deploy(TestVaultV2)
    vault.initialize(token, deployer, rewards, "", "", {"from": deployer})
    vault.setGovernance(deployer, {"from": deployer})
    vault.setRewards(rewards, {"from": deployer})
    vault.setGuardian(deployer, {"from": deployer})
    vault.setDepositLimit(TOTAL_TOKENS, {"from": deployer})

    vault.setManagementFee(0, {"from": deployer})
    vault.setEmergencyShutdown(False, {"from": deployer})
    #vault.setPerformanceFee(PERFORMANCE_FEE, {"from": deployer})

    assert token.balanceOf(vault) == 0
    assert vault.totalDebt() == 0  # No connected strategies yet
    yield vault

@pytest.fixture
def strategy(strategist, deployer, vault, token, investment, StubStrategyV2):
    strategy = strategist.deploy(StubStrategyV2, vault, investment, STUB_YIELD)
    token.approve(strategy, 10**18, {"from":investment})
    strategy.setKeeper(strategist, {"from": strategist})

    # Addresses
    assert strategy.strategist() == strategist
    assert strategy.rewards() == strategist
    assert strategy.keeper() == strategist
    assert strategy.want() == vault.token()
    assert strategy.name() == "StubCurveStrategy"

    assert not strategy.emergencyExit()

    yield strategy

def test_vault_setup_strategy(chain, vault, strategy, token, investment, deployer, strategist, governance, rewards, regular_user):
    vault.addStrategy(strategy, STRAT_DEBT_RATIO, STRAT_OPERATION_LIMIT, STRAT_OPERATION_FEE, {"from": governance})

    assert vault.creditAvailable(strategy) == 0
    assert vault.debtOutstanding(strategy) == 0

    assert strategy.estimatedTotalAssets() == 0

    #deposit to vault
    token.approve(vault, DEPOSIT_VALUE, {"from": regular_user})
    vault.deposit(DEPOSIT_VALUE, {"from": regular_user})

    assert token.balanceOf(vault) == DEPOSIT_VALUE
    assert vault.totalDebt() == 0  # No connected strategies yet
    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE

    #deposit to strategy
    start = chain.time()
    chain.mine(1, start + 2)

    strategy.harvest({"from": strategist})

    strat_info = vault.strategies(strategy)
    strat_debt_ratio = strat_info[2]

    deposit_on_strategy = DEPOSIT_VALUE * strat_debt_ratio / CONST_VAULT_MAX_BPS
    deposit_left_on_vault = DEPOSIT_VALUE - deposit_on_strategy
    #Funds are invested
    assert token.balanceOf(investment) == deposit_on_strategy
    assert vault.totalDebt() == deposit_left_on_vault


    #performace fee is calculated
    YIELD_FEE = ( STUB_YIELD * PERFORMANCE_FEE ) / 10000.0
    STRATEGIST_FEE = int(( STUB_YIELD * STRAT_OPERATION_FEE ) / 10000.0)
    #Calculate estimated shares
    YIELD_FEE_SHARES = calc_shares(token, vault, YIELD_FEE)
    STRATEGIST_FEE_SHARES = calc_shares(token, vault, STRATEGIST_FEE)

    #Earn some yield
    start = chain.time()
    chain.mine(1, start + 2)

    strategy.harvest({"from": strategist})

    assert token.balanceOf(vault) == deposit_left_on_vault + STUB_YIELD #dumb yield generated and transfered as profit to the vault

    #Supply of LP tokens is increased
    assert vault.totalSupply() == DEPOSIT_VALUE + YIELD_FEE_SHARES + STRATEGIST_FEE_SHARES
    assert vault.balanceOf(rewards) == YIELD_FEE_SHARES
    
    sharesCalc = calc_shares(token, vault, WITHDRAW_VALUE)
    #Withdraw some funds
    balance_before = token.balanceOf(regular_user)
    vault.withdraw(WITHDRAW_VALUE, regular_user, {"from": regular_user})
    balance_after = token.balanceOf(regular_user)

    assert token.balanceOf(vault) == (deposit_left_on_vault + STUB_YIELD - sharesCalc)
    assert balance_after - balance_before == sharesCalc #WITHDRAW_VALUE

    sharesCalc = calc_shares(token, vault, vault.balanceOf(regular_user))
    #withdraw all
    balance_before = token.balanceOf(regular_user)
    vault.withdraw({"from": regular_user})
    balance_after = token.balanceOf(regular_user)

    assert balance_after - balance_before == sharesCalc
    assert token.balanceOf(vault) == 0
 