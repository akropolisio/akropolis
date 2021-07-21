import os
import pytest
from dotenv import load_dotenv, find_dotenv
from brownie import *
from brownie import chain
import brownie

SLIPPAGE=1e17
amount=10e18

@pytest.fixture(scope="function", autouse=True)
def isolation(fn_isolation):
    pass



def test_setGovernance(governance, vault_tricrypto, regular_user):
    with brownie.reverts():
        vault_tricrypto.setGovernance(regular_user, {"from": regular_user})


def test_setGaurdian(governance, vault_tricrypto, regular_user):
    with brownie.reverts():
        vault_tricrypto.setGuardian(regular_user, {"from": regular_user})



def test_deposit(vault_tricrypto, regular_user, lpToken, lptoken_owner):
    lpToken.transfer(regular_user, amount, {"from": lptoken_owner})
    assert lpToken.balanceOf(regular_user) == amount
    lpToken.approve(vault_tricrypto.address, amount, {"from": regular_user})
    vault_tricrypto.deposit["uint"](
        amount, {"from": regular_user}
    )
    assert lpToken.balanceOf(regular_user) == 0



def test_withdraw(vault_tricrypto, regular_user, lpToken, lptoken_owner):
    lpToken.transfer(regular_user, amount, {"from": lptoken_owner})
    lpToken.approve(vault_tricrypto.address, amount, {"from": regular_user})
    balanceBefore = lpToken.balanceOf(regular_user)
    vault_tricrypto.deposit["uint"](
        amount, {"from": regular_user}
    )
    assert lpToken.balanceOf(regular_user) == 0
    shares =  vault_tricrypto.balanceOf(regular_user)
    
    vault_tricrypto.withdraw['uint'](shares, {"from": regular_user})
    assert abs(balanceBefore - lpToken.balanceOf(regular_user)) <=SLIPPAGE



def test_emergency_vault_deposit_reverts(lpToken, vault_tricrypto, regular_user, lptoken_owner, governance):

    vault_tricrypto.setEmergencyShutdown(True, {"from": governance})
    

    assert vault_tricrypto.emergencyShutdown() == True
    lpToken.transfer(regular_user, amount, {"from": lptoken_owner})
    lpToken.approve(vault_tricrypto.address, amount, {"from": regular_user})

    with brownie.reverts():
        vault_tricrypto.deposit["uint"].transact(
            amount, {"from": regular_user}
        )

    vault_tricrypto.setEmergencyShutdown(False, {"from": governance})


def test_emergency_vault_withdraw_reverts(lpToken, vault_tricrypto, regular_user, lptoken_owner, governance):

    lpToken.transfer(regular_user, amount, {"from": lptoken_owner})
    lpToken.approve(vault_tricrypto.address, amount, {"from": regular_user})
    vault_tricrypto.deposit["uint"].transact(
        amount, {"from": regular_user}
    )

    vault_tricrypto.setEmergencyShutdown(True, {"from": governance})

    assert vault_tricrypto.emergencyShutdown() == True

    with brownie.reverts():
        vault_tricrypto.withdraw["uint"].transact(
            amount, {"from": regular_user}
        )

    vault_tricrypto.setEmergencyShutdown(False, {"from": governance})
