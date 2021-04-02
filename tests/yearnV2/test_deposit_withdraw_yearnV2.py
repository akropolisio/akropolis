import pytest
import brownie

from constantsV2 import *

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_successful_deposit(token, vault, vaultSavings, register_vault, regular_user, deployer):
    # Initial deposit
    user_balance_before = token.balanceOf(regular_user)
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': regular_user})
    vaultSavings.deposit['address,uint'](vault.address, DEPOSIT_VALUE, {'from': regular_user})

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


def test_successful_withdraw(token, vault, vaultSavings, register_vault, regular_user, deployer):
    # Initial deposits
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': regular_user})
    vaultSavings.deposit['address,uint'](vault.address, DEPOSIT_VALUE, {'from': regular_user})
    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE

    user_balance_before = token.balanceOf(regular_user)

    vault.approve(vaultSavings.address, vault.balanceOf(regular_user), {'from': regular_user})

    # Withdraw the part
    vaultSavings.withdraw['address,uint'].transact(vault.address, WITHDRAW_VALUE, {'from': regular_user})
    
    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE - WITHDRAW_VALUE
    assert vault.totalAssets() == DEPOSIT_VALUE - WITHDRAW_VALUE

    # Withdraw all
    vaultSavings.withdraw['address,uint'].transact(vault.address, vault.balanceOf(regular_user), {'from': regular_user})

    user_balance_after = token.balanceOf(regular_user)

    assert vault.balanceOf(regular_user) == 0
    assert vault.totalAssets() == 0
    # Regular user returns his deposit from the first test
    assert user_balance_after - user_balance_before  == DEPOSIT_VALUE


def test_deposit_zero(register_vault, token, vault, vaultSavings, regular_user):
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': regular_user})
    with brownie.reverts(revert_pattern = "Depositing zero amount"):
        vaultSavings.deposit['address,uint'](vault.address, 0, {'from': regular_user})

def test_withdraw_zero(register_vault, vault, vaultSavings, regular_user):
    vault.approve(vaultSavings.address, vault.balanceOf(regular_user), {'from': regular_user})
    with brownie.reverts(revert_pattern = "Withdrawing zero amount"):
        vaultSavings.withdraw['address,uint'](vault.address, 0, {'from': regular_user})

def calc_amount_for_shares(token, vault, shares):
    return (shares*vault.pricePerShare() // 10 ** token.decimals())

def calc_shares_for_amount(token, vault, amount):
    return (amount * vault.totalSupply()) // (token.balanceOf(vault) + vault.totalDebt())


def calc_exect_shares_for_amount(token, vault, amount):
    s = calc_shares_for_amount(token, vault, amount)
    a = calc_amount_for_shares(token, vault, s)
    if a < amount:
        while a < amount:
            s += 1
            a = calc_amount_for_shares(token, vault, s)
    return s

def test_several_withdraws(chain, token, vault, strategy, vaultSavings, register_vault, regular_user, regular_user2, strategist):
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': regular_user})
    vaultSavings.deposit['address,uint'](vault.address, DEPOSIT_VALUE, {'from': regular_user})

    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': regular_user2})
    vaultSavings.deposit['address,uint'](vault.address, DEPOSIT_VALUE, {'from': regular_user2})

    vault.approve(vaultSavings.address, vault.balanceOf(regular_user), {'from': regular_user})
    vault.approve(vaultSavings.address, vault.balanceOf(regular_user2), {'from': regular_user2})

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

    amount_calculated = calc_amount_for_shares(token, vault,WITHDRAW_VALUE)

    user_balance_before = token.balanceOf(regular_user)
    vaultSavings.withdraw['address,uint'](vault.address, WITHDRAW_VALUE, {'from': regular_user})
    user_balance_after = token.balanceOf(regular_user)

    assert user_balance_after - user_balance_before == amount_calculated

    amount_calculated = calc_amount_for_shares(token, vault, WITHDRAW_VALUE)
    user_balance_before = token.balanceOf(regular_user2)
    vaultSavings.withdraw['address,uint'](vault.address, WITHDRAW_VALUE, {'from': regular_user2})
    user_balance_after = token.balanceOf(regular_user2)

    assert user_balance_after - user_balance_before == amount_calculated

    assert token.balanceOf(vaultSavings) == 0
    assert vault.balanceOf(vaultSavings) == 0