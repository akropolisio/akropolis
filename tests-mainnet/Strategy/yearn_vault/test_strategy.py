from brownie.project import scripts
import pytest
from brownie import *
from brownie import chain
import brownie
from brownie import Contract
import parametrize_from_file

amount = 10e18
SLIPPAGE = 1e17

json_file = "./valide_data.json"


@parametrize_from_file(json_file, "test_parameter")
def test_paramater(yearnVault, regular_user2, lpToken, lptoken_owner, Governance, name):
    contract = Contract.from_explorer(yearnVault)
    lpToken = Contract.from_explorer(lpToken)
    token_owner = accounts.at(lptoken_owner, force=True)
    governance = accounts.at(Governance, force=True)

    # TEST SET GOVERNANCE
    with brownie.reverts():
        contract.setGovernance(regular_user2, {"from": regular_user2})
    # TEST SET GUARDIAN
    with brownie.reverts():
        contract.setGuardian(regular_user2, {"from": regular_user2})
    # TEST DEPOSIT
    lpToken.transfer(regular_user2, amount, {"from": token_owner})
    balanceBefore = lpToken.balanceOf(regular_user2)
    assert lpToken.balanceOf(regular_user2) == amount
    lpToken.approve(contract.address, amount, {"from": regular_user2})
    contract.deposit["uint"](amount, {"from": regular_user2})
    assert lpToken.balanceOf(regular_user2) == 0
    # TEST WITHDRAW
    lpToken.approve(contract.address, amount, {"from": regular_user2})
    shares = contract.balanceOf(regular_user2)

    contract.withdraw["uint"](shares, {"from": regular_user2})
    assert abs(balanceBefore - lpToken.balanceOf(regular_user2)) <= SLIPPAGE

    # EMERGENCY DEPOSIT
    contract.setEmergencyShutdown(True, {"from": governance})
    assert contract.emergencyShutdown() == True
    lpToken.transfer(regular_user2, amount, {"from": token_owner})
    lpToken.approve(contract.address, amount, {"from": regular_user2})
    with brownie.reverts():
        contract.deposit["uint"].transact(amount, {"from": regular_user2})

    contract.setEmergencyShutdown(False, {"from": governance})

    # EMERGENCY WITHDRAW
    contract.setEmergencyShutdown(True, {"from": governance})

    assert contract.emergencyShutdown() == True

    with brownie.reverts():
        contract.withdraw["uint"].transact(amount, {"from": regular_user2})
    contract.setEmergencyShutdown(False, {"from": governance})

    # SEND amount to address lptoken owner
    lpToken.transfer(
        lptoken_owner, lpToken.balanceOf(regular_user2), {"from": regular_user2}
    )
    assert lpToken.balanceOf(regular_user2) == 0
