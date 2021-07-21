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


@pytest.fixture(scope="module")
def register_vault(owner, vault_tricrypto, regular_user, lpToken, lptoken_owner, regular_user1, vault_savings):
    
    assert vault_savings.isVaultRegistered(vault_tricrypto.address) == False
    assert vault_savings.isVaultActive(vault_tricrypto.address) == False

    vault_savings.registerVault(vault_tricrypto.address, {"from": owner})
    vault_savings.activateVault(vault_tricrypto.address, {"from": owner})

    assert vault_savings.isVaultRegistered(vault_tricrypto.address) == True
    assert vault_savings.isVaultActive(vault_tricrypto.address) == True

def test_deposit(
    register_vault, vault_tricrypto, regular_user, lpToken, lptoken_owner, regular_user1, vault_savings,
):  
    lpToken.transfer(regular_user, amount, {"from": lptoken_owner})
    user_balance_before = lpToken.balanceOf(regular_user)
    lpToken.approve(vault_savings.address, amount, {"from": regular_user})
    balance_plugin = lpToken.balanceOf(vault_savings.address)
    assert balance_plugin == 0
    vault_savings.deposit["address,uint"](
        vault_tricrypto.address, amount, {"from": regular_user}
    )
    user_balance_after = lpToken.balanceOf(regular_user)
    assert abs(user_balance_before - user_balance_after) == amount

    #nothing left on the akro_vault
    assert lpToken.balanceOf(vault_savings.address) == 0
    assert vault_tricrypto.balanceOf(vault_savings.address) == 0

    #deposit 0 logic
    lpToken.approve(vault_savings.address, amount, {"from": regular_user})
    with brownie.reverts(revert_pattern="Depositing zero amount"):
        vault_savings.deposit["address,uint"](vault_tricrypto.address, 0, {"from": regular_user})
    

    vault_tricrypto.approve(vault_savings.address, vault_tricrypto.balanceOf(vault_savings.address), {"from": regular_user})
    with brownie.reverts(revert_pattern="Withdrawing zero amount"):
        vault_savings.withdraw["address,uint"](vault_tricrypto.address, 0, {"from": regular_user})
    


    #deposit several times
    lpToken.transfer(regular_user, amount, {"from": lptoken_owner})
    lpToken.transfer(regular_user1, amount, {"from": lptoken_owner})

    lpToken.approve(vault_savings.address, amount, {"from": regular_user})
    
    vault_savings.deposit["address,uint"](
        vault_tricrypto.address, amount, {"from": regular_user}
    )

    assert lpToken.balanceOf(vault_savings.address) == 0
    assert vault_tricrypto.balanceOf(vault_savings.address) == 0


    #add the harvest
    


