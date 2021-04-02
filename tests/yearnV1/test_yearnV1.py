import pytest
import brownie

@pytest.fixture(scope="module")
def register_vault(deployer, token, vault, strategy, controller, registry, vaultSavings):
    controller.setVault(token.address, vault.address, {'from': deployer})
    controller.approveStrategy(token.address, strategy.address, {'from': deployer})
    controller.setStrategy(token.address, strategy.address, {'from': deployer})

    assert registry.getVaultsLength() == 0
    registry.addVault.transact(vault.address, {'from': deployer})
    assert registry.getVaultsLength() == 1
    assert registry.getVault(0) == vault.address
    vaults_arr = registry.getVaults()
    assert len(vaults_arr) == 1
    assert vaults_arr[0] == vault.address

    vaultSavings.registerVault.transact(vault.address, {'from': deployer})
    assert vaultSavings.isVaultRegistered(vault.address) == True
    assert vaultSavings.isVaultActive(vault.address) == True
    assert vaultSavings.isBaseTokenForVault(vault.address, token.address) == True
    supported_vaults = vaultSavings.supportedVaults()
    assert len(supported_vaults) == 1
    assert supported_vaults[0] == vault.address
    active_vaults = vaultSavings.activeVaults()
    assert len(active_vaults) == 1
    assert active_vaults[0] == vault.address

def test_deactivate_vault(register_vault, vaultSavings, vault, deployer):
    vaultSavings.deactivateVault(vault.address, {'from': deployer})

    assert vaultSavings.isVaultActive(vault.address) == False
    active_vaults = vaultSavings.activeVaults()
    assert len(active_vaults) == 0

    vaultSavings.activateVault(vault.address, {'from': deployer})

    assert vaultSavings.isVaultActive(vault.address) == True
    active_vaults = vaultSavings.activeVaults()
    assert len(active_vaults) == 1
    assert active_vaults[0] == vault.address


DEPOSIT_VALUE = 2000000

def test_deposit(register_vault, token, vault, vaultSavings, regular_user, deployer):
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
    assert vault.available() == DEPOSIT_VALUE * vault.min() // vault.max()
    assert token.balanceOf(vault) == DEPOSIT_VALUE


def test_earn():
    # Stub until strategy implemented
    pass

def test_deposit_after_earn():
    # stub until strategy implemented
    pass

def test_withdraw(register_vault, token, vault, vaultSavings, regular_user, deployer):
    user_balance_before = token.balanceOf(regular_user)
    user2_balance_before = token.balanceOf(deployer)

    # Initial deposits
    # Regular user already has deposit from the dirst test
    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE
    #token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': regular_user})
    #vaultSavings.deposit['address,uint'].transact(vault.address, DEPOSIT_VALUE, {'from': regular_user})

    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': deployer})
    vaultSavings.deposit['address,uint'].transact(vault.address, DEPOSIT_VALUE, {'from': deployer})

    # Withdraw
    vault.approve(vaultSavings.address, vault.balanceOf(regular_user), {'from': regular_user})
    vaultSavings.withdraw['address,uint'].transact(vault.address, vault.balanceOf(regular_user), {'from': regular_user})

    vault.approve(vaultSavings.address, vault.balanceOf(deployer), {'from': deployer})
    vaultSavings.withdraw['address,uint'].transact(vault.address, vault.balanceOf(deployer), {'from': deployer})

    user_balance_after = token.balanceOf(regular_user)
    user2_balance_after = token.balanceOf(deployer)

    assert vault.balanceOf(regular_user) == 0
    assert vault.balanceOf(deployer) == 0
    # Regular user returns his deposit from the first test
    assert user_balance_after - user_balance_before  == DEPOSIT_VALUE
    assert user2_balance_before == user2_balance_after


def test_pause_vault(vaultSavings, deployer):
    vaultSavings.pause({'from': deployer})
    assert vaultSavings.paused() == True


def test_pause_unpause_vault(vaultSavings, deployer):
    assert vaultSavings.paused() == True

    vaultSavings.unpause({'from': deployer})
    assert vaultSavings.paused() == False

def test_deposit_unpause_vault_reverts(token, vault, vaultSavings, deployer, regular_user):
    vaultSavings.pause({'from': deployer})
    assert vaultSavings.paused() == True
    with brownie.reverts():
        user_balance_before = token.balanceOf(regular_user)
        token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': regular_user})
        vaultSavings.deposit['address,uint'](vault.address, DEPOSIT_VALUE, {'from': regular_user})
        user_balance_after = token.balanceOf(regular_user)


def test_pause_vault_reverts(vaultSavings, vault, regular_user):
    with brownie.reverts():
        vaultSavings.pause({'from': regular_user})



