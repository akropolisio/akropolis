import pytest
import brownie

from constants import *

def test_register_index(deployer, tokens, uniswap_router, indices_savings_basic):
    lp_index = tokens[TOKEN_INDEX1]
    indices_savings_basic.registerIndex(lp_index, uniswap_router.address, {'from': deployer})
    assert indices_savings_basic.isIndexRegistered(lp_index) == True
    assert indices_savings_basic.isIndexActive(lp_index) == True
    assert indices_savings_basic.getRouterForIndex(lp_index) == uniswap_router.address

    supported_indices = indices_savings_basic.supportedIndices()
    assert len(supported_indices) == 1
    assert supported_indices[0] == lp_index

    active_indices = indices_savings_basic.activeIndices()
    assert len(active_indices) == 1
    assert active_indices[0] == lp_index


def test_deactivate_index(deployer, tokens, indices_savings_basic):
    lp_index = tokens[TOKEN_INDEX1]
    assert indices_savings_basic.isIndexActive(lp_index) == True
    indices_savings_basic.deactivateIndex(lp_index, {'from': deployer})
    assert indices_savings_basic.isIndexActive(lp_index) == False
    assert indices_savings_basic.getRouterForIndex(lp_index) == NULL_ADDRESS

    supported_indices = indices_savings_basic.supportedIndices()
    assert len(supported_indices) == 1
    assert supported_indices[0] == lp_index

    active_indices = indices_savings_basic.activeIndices()
    assert len(active_indices) == 0


def test_activate_index(deployer, tokens, uniswap_router, indices_savings_basic):
    lp_index = tokens[TOKEN_INDEX1]
    assert indices_savings_basic.isIndexActive(lp_index) == False
    indices_savings_basic.activateIndex(lp_index, uniswap_router.address, {'from': deployer})
    assert indices_savings_basic.isIndexActive(lp_index) == True
    assert indices_savings_basic.getRouterForIndex(lp_index) == uniswap_router.address

    supported_indices = indices_savings_basic.supportedIndices()
    assert len(supported_indices) == 1
    assert supported_indices[0] == lp_index

    active_indices = indices_savings_basic.activeIndices()
    assert len(active_indices) == 1


def test_pause_indices(indices_savings_basic, deployer):
    indices_savings_basic.pause({'from': deployer})
    assert indices_savings_basic.paused() == True


def test_pause_unpause_indices(indices_savings_basic, deployer):
    assert indices_savings_basic.paused() == True

    indices_savings_basic.unpause({'from': deployer})
    assert indices_savings_basic.paused() == False


def test_pause_indices_reverts(indices_savings_basic, regular_user):
    with brownie.reverts():
        indices_savings_basic.pause({'from': regular_user})


def test_access_register_index(regular_user, tokens, uniswap_router, indices_savings_basic):
    lp_index = tokens[TOKEN_INDEX2]
    with brownie.reverts(revert_pattern = "Ownable: caller is not the owner"):
        indices_savings_basic.registerIndex(lp_index, uniswap_router.address, {'from': regular_user})


def test_access_deactivate_index(regular_user, tokens, indices_savings_basic):
    lp_index = tokens[TOKEN_INDEX1]
    assert indices_savings_basic.isIndexActive(lp_index) == True
    with brownie.reverts(revert_pattern = "Ownable: caller is not the owner"):
        indices_savings_basic.deactivateIndex(lp_index, {'from': regular_user})


def test_access_activate_index(deployer, regular_user, tokens, uniswap_router, indices_savings_basic):
    lp_index = tokens[TOKEN_INDEX1]
    indices_savings_basic.deactivateIndex(lp_index, {'from': deployer})
    assert indices_savings_basic.isIndexActive(lp_index) == False
    with brownie.reverts(revert_pattern = "Ownable: caller is not the owner"):
        indices_savings_basic.activateIndex(lp_index, uniswap_router.address, {'from': regular_user})



