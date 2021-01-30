import pytest
import brownie
from brownie.test import given, strategy
from hypothesis import settings



#PAUSE/UNPAUSE

DEPOSIT_VALUE = 2000000

@given(
    user=strategy('address', length=10)
)

@settings(max_examples=50)
def test_pause_vault_reverts(vaultSavings, deployer, user):

    if (user == deployer):
        vaultSavings.pause({'from': user});
    else:
        with brownie.reverts():
            vaultSavings.pause({'from': user});



@given(
    user=strategy('address', length=10)
)

@settings(max_examples=50)
def test_deposit_unpause_vault_reverts(token, vault, vaultSavings, deployer, user):
    vaultSavings.pause({'from': deployer});
    assert vaultSavings.paused() == True

    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})

    user_balance_before = token.balanceOf(user)
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})

    with brownie.reverts():
        vaultSavings.deposit['address,uint'](vault.address, DEPOSIT_VALUE, {'from': user})

    vaultSavings.unpause({'from': deployer});

@given(
    user=strategy('address', length=10)
)

@settings(max_examples=50)
def test_deposit_array_unpause_vault_reverts(token, vault, vaultSavings, deployer, user):
    vaultSavings.pause({'from': deployer});
    assert vaultSavings.paused() == True

    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})

    user_balance_before = token.balanceOf(user)
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})

    with brownie.reverts():
        vaultSavings.deposit['address[],uint[]']([vault.address], [DEPOSIT_VALUE], {'from': user})

    vaultSavings.unpause({'from': deployer});



@given(
    user=strategy('address', length=10)
)

@settings(max_examples=50)
def test_deposit_array(register_vault, token, vault, vaultSavings, user, deployer):
    
    assert vaultSavings.paused() == False

    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})
    # Initial deposit
    user_balance_before = token.balanceOf(user)
    vault_token_balance_before = token.balanceOf(vault.address)
    vault_user_balance_before = vault.balanceOf(user)
    
    vault_totalSupply = vault.totalSupply()

    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})
    vaultSavings.deposit['address[],uint[]']([vault.address], [DEPOSIT_VALUE], {'from': user})

    user_balance_after = token.balanceOf(user)
    vault_token_balance_after = token.balanceOf(vault.address)
    vault_user_balance_after = vault.balanceOf(user)

    # User sends tokens and receives LP-tokens
    assert user_balance_before - user_balance_after == DEPOSIT_VALUE
    assert vault_token_balance_after - vault_token_balance_before == DEPOSIT_VALUE

    # First deposit - exect amount
    assert vault_user_balance_after - vault_user_balance_before == DEPOSIT_VALUE
    assert vault.totalSupply() - vault_totalSupply == DEPOSIT_VALUE

    # Nothing left on vaultSavings
    assert vault.balanceOf(vaultSavings.address) == 0
    assert token.balanceOf(vaultSavings.address) == 0

    # For test vault - custom logic
    assert vault.available() == (vault_totalSupply+DEPOSIT_VALUE) * vault.min() // vault.max()
    assert vault.balance() == (vault_totalSupply+DEPOSIT_VALUE)



@given(
    user=strategy('address', length=10)
)
@settings(max_examples=50)
def test_deposit_array(register_vault, token, vault, vaultSavings, user, deployer):
    
    assert vaultSavings.paused() == False

    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})
    # Initial deposit
    user_balance_before = token.balanceOf(user)
    vault_token_balance_before = token.balanceOf(vault.address)
    vault_user_balance_before = vault.balanceOf(user)
    
    vault_totalSupply = vault.totalSupply()
    
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})
    vaultSavings.deposit['address,uint'](vault.address, DEPOSIT_VALUE, {'from': user})

    user_balance_after = token.balanceOf(user)
    vault_token_balance_after = token.balanceOf(vault.address)
    vault_user_balance_after = vault.balanceOf(user)

    # User sends tokens and receives LP-tokens
    assert user_balance_before - user_balance_after == DEPOSIT_VALUE
    assert vault_token_balance_after - vault_token_balance_before == DEPOSIT_VALUE

    # First deposit - exect amount
    assert vault_user_balance_after - vault_user_balance_before == DEPOSIT_VALUE
    assert vault.totalSupply() - vault_totalSupply == DEPOSIT_VALUE

    # Nothing left on vaultSavings
    assert vault.balanceOf(vaultSavings.address) == 0
    assert token.balanceOf(vaultSavings.address) == 0

    # For test vault - custom logic
    assert vault.available() == (vault_totalSupply+DEPOSIT_VALUE) * vault.min() // vault.max()
    assert vault.balance() == (vault_totalSupply+DEPOSIT_VALUE)


@given(
    user=strategy('address', length=10),
    test_vault = strategy('address', length=10),
)

@settings(max_examples=50)

def test_deposit_with_failed_vault(register_vault, token, test_vault, vaultSavings, user, deployer):
    assert vaultSavings.paused() == False

    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})
    
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})

    with brownie.reverts():
        vaultSavings.deposit['address,uint'](test_vault, DEPOSIT_VALUE, {'from': user})

@given(
    user=strategy('address', length=10),
    test_vault = strategy('address', length=10),
)

@settings(max_examples=50)
def test_deposit_array_with_failed_vault(register_vault, token, test_vault, vaultSavings, user, deployer):
    assert vaultSavings.paused() == False

    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})
    
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})

    with brownie.reverts():
        vaultSavings.deposit['address[],uint[]']([test_vault], [DEPOSIT_VALUE], {'from': user})



@given(
    user=strategy('address', length=10),
    user2=strategy('address', length=10)
)

@settings(max_examples=50)

def test_withdraw(register_vault, token, vault, vaultSavings, user, user2, deployer):
    
    if (user != user2):
        token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})
        token.transfer(user2, DEPOSIT_VALUE,  {"from": deployer})

        user_balance_before = token.balanceOf(user) #2000
        user2_balance_before = token.balanceOf(user2) #4000

        vault_user_balance_before = vault.balanceOf(user)
        vault_user2_balance_before = vault.balanceOf(user2)

        # Initial deposits

        token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})
        vaultSavings.deposit['address,uint'].transact(vault.address, DEPOSIT_VALUE, {'from': user})

        token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user2})
        vaultSavings.deposit['address,uint'].transact(vault.address, DEPOSIT_VALUE, {'from': user2})


        assert token.balanceOf(user)+DEPOSIT_VALUE == user_balance_before
        assert token.balanceOf(user2)+DEPOSIT_VALUE == user2_balance_before

        # Withdraw
        vault.approve(vaultSavings.address, vault.balanceOf(user), {'from': user})
        vaultSavings.withdraw['address,uint'].transact(vault.address, vault.balanceOf(user), {'from': user})

        vault.approve(vaultSavings.address, vault.balanceOf(user2), {'from': user2})
        vaultSavings.withdraw['address,uint'].transact(vault.address, vault.balanceOf(user2), {'from': user2})


        # Nothing left on vaultSavings
        assert vault.balanceOf(vaultSavings.address) == 0
        assert token.balanceOf(vaultSavings.address) == 0

        user_balance_after = token.balanceOf(user)
        user2_balance_after = token.balanceOf(user2)

        vault_user_balance_after = vault.balanceOf(user)
        vault_user2_balance_after = vault.balanceOf(user2)

        assert vault_user_balance_after == 0
        assert vault_user2_balance_after == 0

        if (vault_user_balance_before == 0):
            assert user_balance_before == user_balance_after
        else:
            assert user_balance_after == user_balance_before+DEPOSIT_VALUE
        
       
        if (vault_user2_balance_before == 0):
            assert user2_balance_before == user2_balance_after
        else:
            assert user2_balance_after == user2_balance_before+DEPOSIT_VALUE
    else: 
        pass


@given(
    user=strategy('address', length=10),
    user2=strategy('address', length=10)
)

@settings(max_examples=50)

def test_withdraw_array(register_vault, token, vault, vaultSavings, user, user2, deployer):
    
    if (user != user2):
        token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})
        token.transfer(user2, DEPOSIT_VALUE,  {"from": deployer})

        user_balance_before = token.balanceOf(user) #2000
        user2_balance_before = token.balanceOf(user2) #4000

        vault_user_balance_before = vault.balanceOf(user)
        vault_user2_balance_before = vault.balanceOf(user2)

        # Initial deposits

        token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})
        vaultSavings.deposit['address[],uint[]'].transact([vault.address], [DEPOSIT_VALUE], {'from': user})

        token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user2})
        vaultSavings.deposit['address[],uint[]'].transact([vault.address], [DEPOSIT_VALUE], {'from': user2})


        assert token.balanceOf(user)+DEPOSIT_VALUE == user_balance_before
        assert token.balanceOf(user2)+DEPOSIT_VALUE == user2_balance_before

        # Withdraw
        vault.approve(vaultSavings.address, vault.balanceOf(user), {'from': user})
        vaultSavings.withdraw['address[],uint[]'].transact([vault.address], [vault.balanceOf(user)], {'from': user})

        vault.approve(vaultSavings.address, vault.balanceOf(user2), {'from': user2})
        vaultSavings.withdraw['address[],uint[]'].transact([vault.address], [vault.balanceOf(user2)], {'from': user2})


        # Nothing left on vaultSavings
        assert vault.balanceOf(vaultSavings.address) == 0
        assert token.balanceOf(vaultSavings.address) == 0

        user_balance_after = token.balanceOf(user)
        user2_balance_after = token.balanceOf(user2)

        vault_user_balance_after = vault.balanceOf(user)
        vault_user2_balance_after = vault.balanceOf(user2)

        assert vault_user_balance_after == 0
        assert vault_user2_balance_after == 0

        if (vault_user_balance_before == 0):
            assert user_balance_before == user_balance_after
        else:
            assert user_balance_after == user_balance_before+DEPOSIT_VALUE
        
       
        if (vault_user2_balance_before == 0):
            assert user2_balance_before == user2_balance_after
        else:
            assert user2_balance_after == user2_balance_before+DEPOSIT_VALUE
    else: 
        pass


@given(
    user=strategy('address', length=10),
    vault2=strategy('address', length=10)
)
@settings(max_examples=50)
def test_deposit_array_valid_faild_vaults(register_vault, token, vault, vaultSavings, user, vault2, deployer):
    
    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})
    with brownie.reverts():
        vaultSavings.deposit['address[],uint[]']([vault.address, vault2], [DEPOSIT_VALUE, DEPOSIT_VALUE], {'from': user})



@given(
    user=strategy('address', length=10),
    vault2=strategy('address', length=10)
)
@settings(max_examples=50)
def test_withdraw_array_valid_faild_vaults(register_vault, token, vault, vaultSavings, user, vault2, deployer):
    
    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})
    vaultSavings.deposit['address[],uint[]'].transact([vault.address], [DEPOSIT_VALUE], {'from': user})

    vault.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})

    with brownie.reverts():
        vaultSavings.withdraw['address[],uint[]'].transact([vault.address, vault2], [DEPOSIT_VALUE, DEPOSIT_VALUE], {'from': user})



@given(
    user=strategy('address', length=10)
)

@settings(max_examples=50)
def test_deposit_deactivated_vault_reverts(token, vault, vaultSavings, deployer, user):

    vaultSavings.deactivateVault(vault.address, {'from': deployer})

    assert vaultSavings.isVaultActive(vault.address) == False

    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})
    with brownie.reverts():
        vaultSavings.deposit['address,uint'](vault.address, DEPOSIT_VALUE, {'from': user})

    vaultSavings.activateVault(vault.address, {'from': deployer})


@given(
    user=strategy('address', length=10)
)

@settings(max_examples=50)
def test_withdraw_deactivated_vault_reverts(token, vault, vaultSavings, deployer, user):
    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})
    vaultSavings.deposit['address[],uint[]'].transact([vault.address], [DEPOSIT_VALUE], {'from': user})
    vault.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})
    vaultSavings.deactivateVault(vault.address, {'from': deployer})

    assert vaultSavings.isVaultActive(vault.address) == False

    with brownie.reverts():
        vaultSavings.withdraw['address[],uint[]'].transact([vault.address], [DEPOSIT_VALUE], {'from': user})

    vaultSavings.activateVault(vault.address, {'from': deployer})



@given(
    user=strategy('address', length=10)
)
@settings(max_examples=50)
def test_activated_vault_reverts(token, vault, vaultSavings, deployer, user):
   
    with brownie.reverts():
        vaultSavings.activateVault(vault.address, {'from': user})

    vaultSavings.activateVault(vault.address, {'from': deployer})


@given(
    user=strategy('address', length=10)
)
@settings(max_examples=50)
def test_deactivated_vault_reverts(token, vault, vaultSavings, deployer, user):
   
    with brownie.reverts():
        vaultSavings.deactivateVault(vault.address, {'from': user})

    vaultSavings.activateVault(vault.address, {'from': deployer})


@given(
    user=strategy('address', length=10)
)
@settings(max_examples=50)
def test_owner_not_changed(token, vault, vaultSavings, deployer, user):
    token.transfer(user, DEPOSIT_VALUE,  {"from": deployer})
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})
    vault.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': user})
    vaultSavings.deposit['address[],uint[]'].transact([vault.address], [DEPOSIT_VALUE], {'from': user})
    vaultSavings.withdraw['address[],uint[]'].transact([vault.address], [DEPOSIT_VALUE], {'from': user})

    assert vaultSavings.owner() == deployer
