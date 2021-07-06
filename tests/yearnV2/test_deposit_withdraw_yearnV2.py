import pytest
import brownie

from constantsV2 import *


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_successful_deposit(
    token, vault, vaultSavings, register_vault, regular_user, deployer
):
    # Initial deposit
    user_balance_before = token.balanceOf(regular_user)
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {"from": regular_user})
    vaultSavings.deposit["address,uint"](
        vault.address, DEPOSIT_VALUE, {"from": regular_user}
    )

    user_balance_after = token.balanceOf(regular_user)

    # User sends tokens and receives LP-tokens
    assert user_balance_before - user_balance_after == DEPOSIT_VALUE
    assert token.balanceOf(vault.address) == DEPOSIT_VALUE

    # First deposit - exect amount
    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE
    assert vault.totalSupply() == DEPOSIT_VALUE

    # Nothing left on vaultSavings
    assert vault.balanceOf(vaultSavings.address) == 0
    assert token.balanceOf(vaultSavings.address) == 0

    # For test vault - custom logic
    assert token.balanceOf(vault.address) == DEPOSIT_VALUE
    assert vault.totalAssets() == DEPOSIT_VALUE


def test_successful_withdraw(
    token, vault, vaultSavings, register_vault, regular_user, deployer
):
    # Initial deposits
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {"from": regular_user})
    vaultSavings.deposit["address,uint"](
        vault.address, DEPOSIT_VALUE, {"from": regular_user}
    )
    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE

    user_balance_before = token.balanceOf(regular_user)

    vault.approve(
        vaultSavings.address, vault.balanceOf(regular_user), {"from": regular_user}
    )

    # Withdraw the part
    vaultSavings.withdraw["address,uint"].transact(
        vault.address, WITHDRAW_VALUE, {"from": regular_user}
    )

    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE - WITHDRAW_VALUE
    assert vault.totalAssets() == DEPOSIT_VALUE - WITHDRAW_VALUE

    # Withdraw all
    vaultSavings.withdraw["address,uint"].transact(
        vault.address, vault.balanceOf(regular_user), {"from": regular_user}
    )

    user_balance_after = token.balanceOf(regular_user)

    assert vault.balanceOf(regular_user) == 0
    assert vault.totalAssets() == 0
    # Regular user returns his deposit from the first test
    assert user_balance_after - user_balance_before == DEPOSIT_VALUE


def test_deposit_zero(register_vault, token, vault, vaultSavings, regular_user):
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {"from": regular_user})
    with brownie.reverts(revert_pattern="Depositing zero amount"):
        vaultSavings.deposit["address,uint"](vault.address, 0, {"from": regular_user})


def test_withdraw_zero(register_vault, vault, vaultSavings, regular_user):
    vault.approve(
        vaultSavings.address, vault.balanceOf(regular_user), {"from": regular_user}
    )
    with brownie.reverts(revert_pattern="Withdrawing zero amount"):
        vaultSavings.withdraw["address,uint"](vault.address, 0, {"from": regular_user})


def calc_amount_for_shares(token, vault, shares):
    return (token.balanceOf(vault) + vault.totalDebt()) * shares // vault.totalSupply()


def calc_shares_for_amount(token, vault, amount):
    return (amount * vault.totalSupply()) // (
        token.balanceOf(vault) + vault.totalDebt()
    )


def calc_exect_shares_for_amount(token, vault, amount):
    s = calc_shares_for_amount(token, vault, amount)
    a = calc_amount_for_shares(token, vault, s)
    if a < amount:
        while a < amount:
            s += 1
            a = calc_amount_for_shares(token, vault, s)
    return s


def test_deposit_yield_withdraw(
    chain,
    token,
    vault,
    strategy,
    vaultSavings,
    register_vault,
    regular_user,
    strategist,
):
    strat_info = vault.strategies(strategy)
    strat_debt_ratio = strat_info[2]

    # Deposit
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {"from": regular_user})
    vaultSavings.deposit["address,uint"](
        vault.address, DEPOSIT_VALUE, {"from": regular_user}
    )

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0

    # All funds are in the vault before the harvesting starts
    assert token.balanceOf(vault) == DEPOSIT_VALUE
    assert vault.totalDebt() == 0  # No connected strategies yet
    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE
    assert vault.totalAssets() == DEPOSIT_VALUE

    # Strategy takes money from the Vault.
    start = chain.time()
    chain.mine(1, start + 2)

    strategy.harvest({"from": strategist})

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0

    # No yield for the first time (since no money were on the strategy)
    assert vault.totalAssets() == DEPOSIT_VALUE

    # Strategy operation is limited to its debt ratio
    deposit_on_strategy = DEPOSIT_VALUE * strat_debt_ratio / CONST_VAULT_MAX_BPS
    deposit_left_on_vault = DEPOSIT_VALUE - deposit_on_strategy
    # Funds are invested
    assert strategy.estimatedTotalAssets() == deposit_on_strategy
    assert vault.totalDebt() == deposit_on_strategy
    assert token.balanceOf(vault) == deposit_left_on_vault

    # Particular withdraw
    vault.approve(
        vaultSavings.address, vault.balanceOf(regular_user), {"from": regular_user}
    )

    user_balance_before = token.balanceOf(regular_user)
    vaultSavings.withdraw["address,uint"](
        vault.address, WITHDRAW_VALUE, {"from": regular_user}
    )
    user_balance_after = token.balanceOf(regular_user)

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0

    # Since there are funds in the vault - withdraws from the vault
    # Sinve no yield yet - no comissions
    assert (
        strategy.estimatedTotalAssets() == deposit_on_strategy
    )  # No changes for the strategy yet
    assert user_balance_after - user_balance_before == WITHDRAW_VALUE
    assert token.balanceOf(vault) == deposit_left_on_vault - WITHDRAW_VALUE
    assert vault.totalAssets() == DEPOSIT_VALUE - WITHDRAW_VALUE

    # New vaults balance
    deposit_left_on_vault -= WITHDRAW_VALUE

    # Strategy takes money from the Vault and generates yield
    start = chain.time()
    chain.mine(1, start + 2)

    strategy.harvest({"from": strategist})

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0

    assert (
        token.balanceOf(vault) == deposit_left_on_vault + STUB_YIELD
    )  # Yield goes to vault
    # No new debts for the vault - nothing deposited, so strategy is already full
    assert strategy.estimatedTotalAssets() == deposit_on_strategy
    assert vault.totalAssets() == DEPOSIT_VALUE - WITHDRAW_VALUE + STUB_YIELD

    shares_to_withdraw = calc_exect_shares_for_amount(
        token, vault, deposit_left_on_vault
    )

    # Withdraw all from the vault except the yield
    vaultSavings.withdraw["address,uint"](
        vault.address, shares_to_withdraw, {"from": regular_user}
    )
    assert token.balanceOf(vault) == STUB_YIELD
    assert strategy.estimatedTotalAssets() == deposit_on_strategy

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0

    YIELD_FEE = (STUB_YIELD * PERFORMANCE_FEE) // 10000
    STRATEGIST_FEE = (STUB_YIELD * STRAT_OPERATION_FEE) // 10000
    REAL_YIELD = STUB_YIELD - YIELD_FEE - STRATEGIST_FEE

    # Withdraw all - part from the vault and part from the strategy
    user_balance_before = token.balanceOf(regular_user)
    vaultSavings.withdraw["address,uint"](
        vault.address, vault.balanceOf(regular_user), {"from": regular_user}
    )
    user_balance_after = token.balanceOf(regular_user)

    ####
    # Here is a problem in math - we always loose 1 token because of roundings
    ####
    assert (
        user_balance_after - user_balance_before == REAL_YIELD + deposit_on_strategy - 1
    )
    assert vault.totalAssets() == YIELD_FEE + STRATEGIST_FEE + 1

    assert vault.balanceOf(regular_user) == 0

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0


def test_several_deposits(
    chain,
    token,
    vault,
    strategy,
    vaultSavings,
    register_vault,
    regular_user,
    regular_user2,
    strategist,
):
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {"from": regular_user})
    vaultSavings.deposit["address,uint"](
        vault.address, DEPOSIT_VALUE, {"from": regular_user}
    )

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0

    start = chain.time()
    chain.mine(1, start + 2)

    strategy.harvest({"from": strategist})

    # No yield yet
    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0

    start = chain.time()
    chain.mine(1, start + 2)

    strategy.harvest({"from": strategist})
    YIELD_FEE = (STUB_YIELD * PERFORMANCE_FEE) // 10000
    STRATEGIST_FEE = (STUB_YIELD * STRAT_OPERATION_FEE) // 10000

    fee_shares = calc_exect_shares_for_amount(token, vault, YIELD_FEE + STRATEGIST_FEE)
    # Yield mined

    new_user_shares = calc_shares_for_amount(token, vault, DEPOSIT_VALUE)

    token.approve(vaultSavings.address, DEPOSIT_VALUE, {"from": regular_user2})
    vaultSavings.deposit["address,uint"](
        vault.address, DEPOSIT_VALUE, {"from": regular_user2}
    )

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0

    # Check that all is calculated correctly and users are not affected
    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE  # Not changed
    assert vault.balanceOf(regular_user2) == new_user_shares  # calculated correctly
    assert vault.totalSupply() == DEPOSIT_VALUE + new_user_shares + fee_shares
    assert (
        token.balanceOf(vault) + strategy.estimatedTotalAssets()
        == DEPOSIT_VALUE + DEPOSIT_VALUE + STUB_YIELD
    )  # No extra funds or missing funds


def test_several_withdraws(
    chain,
    token,
    vault,
    strategy,
    vaultSavings,
    register_vault,
    regular_user,
    regular_user2,
    strategist,
):
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {"from": regular_user})
    vaultSavings.deposit["address,uint"](
        vault.address, DEPOSIT_VALUE, {"from": regular_user}
    )

    token.approve(vaultSavings.address, DEPOSIT_VALUE, {"from": regular_user2})
    vaultSavings.deposit["address,uint"](
        vault.address, DEPOSIT_VALUE, {"from": regular_user2}
    )

    vault.approve(
        vaultSavings.address, vault.balanceOf(regular_user), {"from": regular_user}
    )
    vault.approve(
        vaultSavings.address, vault.balanceOf(regular_user2), {"from": regular_user2}
    )

    start = chain.time()
    chain.mine(1, start + 2)

    strategy.harvest({"from": strategist})

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0

    start = chain.time()
    chain.mine(1, start + 2)

    strategy.harvest({"from": strategist})

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0

    amount_calculated = calc_amount_for_shares(token, vault, WITHDRAW_VALUE)
    user_balance_before = token.balanceOf(regular_user)
    vaultSavings.withdraw["address,uint"](
        vault.address, WITHDRAW_VALUE, {"from": regular_user}
    )
    user_balance_after = token.balanceOf(regular_user)

    assert user_balance_after - user_balance_before == amount_calculated

    amount_calculated = calc_amount_for_shares(token, vault, WITHDRAW_VALUE)
    user_balance_before = token.balanceOf(regular_user2)
    vaultSavings.withdraw["address,uint"](
        vault.address, WITHDRAW_VALUE, {"from": regular_user2}
    )
    user_balance_after = token.balanceOf(regular_user2)

    assert user_balance_after - user_balance_before == amount_calculated

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0


def test_deposit_yield_withdraw_two_strategies(
    vault_add_second_strategy,
    chain,
    token,
    vault,
    strategy,
    strategy2,
    vaultSavings,
    regular_user,
    strategist,
):
    strat_info = vault.strategies(strategy)
    strat_debt_ratio = strat_info[2]

    strat_info2 = vault.strategies(strategy2)
    strat_debt_ratio2 = strat_info2[2]

    token.approve(vaultSavings.address, DEPOSIT_VALUE, {"from": regular_user})
    vaultSavings.deposit["address,uint"](
        vault.address, DEPOSIT_VALUE, {"from": regular_user}
    )

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE

    start = chain.time()
    chain.mine(1, start + 2)

    strategy.harvest({"from": strategist})
    strategy2.harvest({"from": strategist})

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE

    deposit_on_strategy = DEPOSIT_VALUE * strat_debt_ratio / CONST_VAULT_MAX_BPS
    deposit_on_strategy2 = DEPOSIT_VALUE * strat_debt_ratio2 / CONST_VAULT_MAX_BPS
    assert strategy.estimatedTotalAssets() == deposit_on_strategy
    assert strategy2.estimatedTotalAssets() == deposit_on_strategy2

    start = chain.time()
    chain.mine(1, start + 2)

    strategy.harvest({"from": strategist})
    strategy2.harvest({"from": strategist})

    YIELD_FEE = (STUB_YIELD * PERFORMANCE_FEE) // 10000
    STRATEGIST_FEE = (STUB_YIELD * STRAT_OPERATION_FEE) // 10000

    vault.approve(vaultSavings, vault.balanceOf(regular_user), {"from": regular_user})
    user_balance_before = token.balanceOf(regular_user)
    vaultSavings.withdraw["address,uint"](
        vault.address, vault.balanceOf(regular_user), {"from": regular_user}
    )
    user_balance_after = token.balanceOf(regular_user)

    ###
    # Again - here we loose 1 token within the math
    ###
    assert (
        user_balance_after - user_balance_before
        == DEPOSIT_VALUE + 2 * (STUB_YIELD - YIELD_FEE - STRATEGIST_FEE) - 1
    )

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(regular_user) == 0


def test_deposit_withdraw_several_vaults(
    register_vault2,
    chain,
    token,
    vault,
    strategy,
    token2,
    vault2,
    strategy_vault2,
    vaultSavings,
    regular_user,
    strategist,
):
    strat_info = vault.strategies(strategy)
    strat_debt_ratio = strat_info[2]

    strat_info2 = vault2.strategies(strategy_vault2)
    strat_debt_ratio2 = strat_info2[2]

    token.approve(vaultSavings.address, DEPOSIT_VALUE, {"from": regular_user})
    token2.approve(vaultSavings.address, DEPOSIT_VALUE, {"from": regular_user})
    vaultSavings.deposit["address[],uint[]"](
        [vault.address, vault2.address],
        [DEPOSIT_VALUE, DEPOSIT_VALUE],
        {"from": regular_user},
    )

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE

    assert token2.balanceOf(vaultSavings) == 0
    assert vault2.balanceOf(vaultSavings) == 0
    assert vault2.balanceOf(regular_user) == DEPOSIT_VALUE

    start = chain.time()
    chain.mine(1, start + 2)

    strategy.harvest({"from": strategist})
    strategy_vault2.harvest({"from": strategist})

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE

    assert token2.balanceOf(vaultSavings) == 0
    assert vault2.balanceOf(vaultSavings) == 0
    assert vault2.balanceOf(regular_user) == DEPOSIT_VALUE

    deposit_on_strategy = DEPOSIT_VALUE * strat_debt_ratio / CONST_VAULT_MAX_BPS
    deposit_on_strategy2 = DEPOSIT_VALUE * strat_debt_ratio2 / CONST_VAULT_MAX_BPS
    assert strategy.estimatedTotalAssets() == deposit_on_strategy
    assert strategy_vault2.estimatedTotalAssets() == deposit_on_strategy2

    vault.approve(vaultSavings, vault.balanceOf(regular_user), {"from": regular_user})
    vault2.approve(vaultSavings, vault2.balanceOf(regular_user), {"from": regular_user})
    vaultSavings.withdraw["address[],uint[]"](
        [vault.address, vault2.address],
        [DEPOSIT_VALUE, DEPOSIT_VALUE],
        {"from": regular_user},
    )

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(regular_user) == 0

    assert token2.balanceOf(vaultSavings) == 0
    assert vault2.balanceOf(vaultSavings) == 0
    assert vault2.balanceOf(regular_user) == 0
