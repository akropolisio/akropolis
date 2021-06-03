import pytest
import brownie

EPOCH_LENGTH = 100


def test_vakro_rate(chain, deployer, akro, vakro, regular_user):
    vakro.setVestingCliff(0, {"from": deployer})
    start = chain.time() + 1000
    vakro.setVestingStart(start, {"from": deployer})
    ###
    # Add some vakro for the user
    ###
    vakro.mint(deployer, 1000, {"from": deployer})
    vakro.transfer(regular_user, 1000, {"from": deployer})

    akro.approve(vakro.address, 2500, {"from": deployer})
    vakro.addAkroLiquidity(2500, {"from": deployer})

    locked, unlocked, unlockable = vakro.balanceInfoOf(regular_user)
    assert locked == 1000
    assert unlocked == 0
    assert unlockable == 0

    assert vakro.balanceOfAkro(regular_user) == 1000
    assert vakro.balanceOf(regular_user) == 1000

    akro_balance_before = akro.balanceOf(regular_user)

    ###
    # Unlock the funds
    ###
    chain.mine(1, start + EPOCH_LENGTH // 2)  # unlock half of the funds

    locked, unlocked, unlockable = vakro.balanceInfoOf(regular_user)
    assert locked == 1000  # half
    assert unlocked == 0
    assert unlockable == 500  # half

    assert vakro.balanceOfAkro(regular_user) == 1000
    assert vakro.balanceOf(regular_user) == 1000

    akro_balance_after = akro.balanceOf(regular_user)
    assert akro_balance_before == akro_balance_after

    vakro.unlockAvailable(regular_user, {"from": regular_user})

    ###
    # Claim unlocked
    ###
    locked, unlocked, unlockable = vakro.balanceInfoOf(regular_user)

    vakro.redeemAllUnlocked({"from": regular_user})

    assert vakro.balanceOfAkro(regular_user) == locked

    akro_balance_after = akro.balanceOf(regular_user)
    assert akro_balance_after - akro_balance_before == unlocked  # half redeemed

    ###
    # Change rates
    ###
    vakro_balance_before = vakro.balanceOf(regular_user)
    vakro.setSwapRate(4, 1, {"from": deployer})  # 1 vAkro = 4 AKRO

    ###
    # Unlock the funds with new rate
    ###
    chain.mine(1, start + EPOCH_LENGTH)  # unlock all the funds

    locked, unlocked, unlockable = vakro.balanceInfoOf(regular_user)

    assert vakro.balanceOfAkro(regular_user) == locked * 4  # 500 x4
    vakro_balance_after = vakro.balanceOf(regular_user)

    assert vakro_balance_before == vakro_balance_after

    vakro.unlockAvailable(regular_user, {"from": regular_user})

    locked, unlocked, unlockable = vakro.balanceInfoOf(regular_user)

    assert vakro.balanceOfAkro(regular_user) == unlocked * 4

    ###
    # Claim unlocked with new rate
    ###

    vakro.redeemAllUnlocked({"from": regular_user})

    locked, unlocked, unlockable = vakro.balanceInfoOf(regular_user)
    assert locked == 0
    assert unlocked == 0
    assert unlockable == 0

    assert vakro.balanceOfAkro(regular_user) == 0
    assert vakro.balanceOf(regular_user) == 0

    akro_balance_after = akro.balanceOf(regular_user)
    assert akro_balance_after - akro_balance_before == 2500  # all redeemed
