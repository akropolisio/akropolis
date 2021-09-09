from brownie.project import scripts
import pytest
from brownie import *
from brownie import chain
import brownie
from brownie import Contract
import parametrize_from_file

amount = 10e18
SLIPPAGE = 1e17
ACCURACY = 10e12

json_file = "./valide_data.json"


@parametrize_from_file(json_file, "test_parameter")
def test_full_workflow(
    yearnVault,
    regular_user,
    lpToken,
    lptoken_owner,
    Governance,
    vault_savings,
    owner,
    regular_user1,
    Voter,
    Strategist,
    name,
):
    # REGISTER THE VAULT
    contract = Contract.from_explorer(yearnVault)
    lpToken = Contract.from_explorer(lpToken)
    lpToken_owner = accounts.at(lptoken_owner, force=True)
    governance = accounts.at(Governance, force=True)
    voters = contract.from_explorer(Voter)
    strategist = accounts.at(Strategist, force=True)
    if vault_savings.isVaultRegistered(contract.address) == False:
        vault_savings.registerVault(contract.address, {"from": owner})
    if vault_savings.isVaultActive(contract.address) == False:
        vault_savings.activateVault(contract.address, {"from": owner})

    assert vault_savings.isVaultRegistered(contract.address) == True
    assert vault_savings.isVaultActive(contract.address) == True
    lpToken.transfer(regular_user, amount, {"from": lptoken_owner})
    user_balance_before = lpToken.balanceOf(regular_user)
    lpToken.approve(vault_savings.address, amount, {"from": regular_user})
    balance_plugin = lpToken.balanceOf(vault_savings.address)
    yearn_balance_before = lpToken.balanceOf(contract)
    assert balance_plugin == 0
    tx = vault_savings.deposit["address,uint"](
        contract.address, amount, {"from": regular_user}
    )
    balanceProofTokenLiquidity1 = contract.balanceOf(regular_user)
    deposit_amount = tx.return_value
    user_balance_after = lpToken.balanceOf(regular_user)
    assert abs(user_balance_before - user_balance_after) == amount
    assert lpToken.balanceOf(contract) - amount == yearn_balance_before

    # nothing left on the akro_vault
    assert lpToken.balanceOf(vault_savings.address) == 0
    assert contract.balanceOf(vault_savings.address) == 0
    assert deposit_amount == contract.balanceOf(regular_user)

    # deposit 0 logic
    lpToken.approve(vault_savings.address, amount, {"from": regular_user})
    with brownie.reverts("Depositing zero amount"):
        vault_savings.deposit["address,uint"](
            contract.address, 0, {"from": regular_user}
        )

    contract.approve(
        vault_savings.address,
        contract.balanceOf(vault_savings.address),
        {"from": regular_user},
    )
    with brownie.reverts("Withdrawing zero amount"):
        vault_savings.withdraw["address,uint"](
            contract.address, 0, {"from": regular_user}
        )

    reg_1_balance_before = contract.balanceOf(regular_user)
    reg_2_balance_before = contract.balanceOf(regular_user1)
    balance_plugin_before = lpToken.balanceOf(contract.address)
    # deposit several times
    lpToken.transfer(regular_user, amount, {"from": lptoken_owner})

    lpToken.approve(vault_savings.address, amount, {"from": regular_user})

    vault_savings.deposit["address,uint"](
        contract.address, amount, {"from": regular_user}
    )
    # second user deposit
    lpToken.transfer(regular_user1, amount, {"from": lptoken_owner})

    lpToken.approve(vault_savings.address, amount, {"from": regular_user1})

    vault_savings.deposit["address,uint"](
        contract.address, amount, {"from": regular_user1}
    )

    balanceProofTokenLiquidity2 = contract.balanceOf(regular_user1)

    assert lpToken.balanceOf(vault_savings.address) == 0
    assert lpToken.balanceOf(contract) > balance_plugin_before
    assert contract.balanceOf(vault_savings.address) == 0
    assert lpToken.balanceOf(regular_user) == 0
    assert contract.balanceOf(regular_user) > reg_1_balance_before
    assert contract.balanceOf(regular_user1) > reg_2_balance_before
    chain.snapshot()

    # withdraw user 1
    contract.approve(
        vault_savings.address, balanceProofTokenLiquidity1, {"from": regular_user}
    )
    vault_savings.withdraw["address,uint"].transact(
        contract.address, balanceProofTokenLiquidity1, {"from": regular_user}
    )

    balanceWithdraw = lpToken.balanceOf(regular_user)
    assert abs(balanceWithdraw - amount) <= ACCURACY

    chain.revert()
    # harvest
    chain.sleep(1209600)
    voters.harvest({"from": strategist})
    chain.mine(100)

    contract.approve(
        vault_savings.address, balanceProofTokenLiquidity1, {"from": regular_user}
    )
    vault_savings.withdraw["address,uint"].transact(
        contract.address, balanceProofTokenLiquidity1, {"from": regular_user}
    )

    balancelpAfterHarvest = lpToken.balanceOf(regular_user)

    assert abs(balancelpAfterHarvest - balanceWithdraw) <= SLIPPAGE

    chain.mine(100)

    # user 2 withdraw
    contract.approve(
        vault_savings.address, balanceProofTokenLiquidity2, {"from": regular_user1}
    )
    vault_savings.withdraw["address,uint"].transact(
        contract.address, balanceProofTokenLiquidity2, {"from": regular_user1}
    )

    assert abs(lpToken.balanceOf(regular_user1) - amount) <= SLIPPAGE

    lpToken.transfer(
        lpToken_owner, lpToken.balanceOf(regular_user), {"from": regular_user}
    )
    assert lpToken.balanceOf(regular_user) == 0
