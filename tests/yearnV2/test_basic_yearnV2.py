import pytest
import brownie

from constantsV2 import *

@pytest.fixture(scope="module")
def register_vault(deployer, token, vault, strategy, registry, vaultSavings):
    assert registry.vaults(token.address, 0) == NULL_ADDRESS
    registry.newRelease(vault.address, {'from': deployer})
    registry.endorseVault(vault.address, {"from": deployer})
    
    assert registry.vaults(token.address, 0) == vault.address

    vaultSavings.registerVault(vault.address, {'from': deployer})
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



