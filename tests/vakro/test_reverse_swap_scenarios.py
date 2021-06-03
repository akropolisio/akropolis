import pytest
import brownie

ADEL_TO_SWAP = 100
AKRO_ON_SWAP = 10000
ADEL_AKRO_RATE = 15
EPOCH_LENGTH = 100
REWARDS_AMOUNT = 150
ADEL_MAX_ALLOWED = 1000
NULL_ADDRESS = "0x0000000000000000000000000000000000000000"
ADEL_REWARDS_TO_SWAP = 150
ADEL_WALLET_VESTING_REWARDS_TO_SWAP = 175
ADEL_REWARDS_MAX_ALLOWED = 1050
ADEL_WALLET_VESTING_REWARDS_MAX_ALLOWED = 1200
ADEL_TOTAL_VESTING_REWARDS_MAX_ALLOWED = 2000


@pytest.fixture(scope="module")
def prepare_swap(
    chain, deployer, adel, akro, vakro, stakingpool, testVakroSwap, testVakroVestingSwap
):
    vakro.addMinter(testVakroSwap.address, {"from": deployer})
    vakro.addSender(testVakroSwap.address, {"from": deployer})

    vakro.addMinter(testVakroVestingSwap.address, {"from": deployer})
    vakro.addSender(testVakroVestingSwap.address, {"from": deployer})

    adel.addMinter(testVakroSwap.address, {"from": deployer})

    stakingpool.setSwapContract(testVakroSwap.address, {"from": deployer})

    tx = testVakroSwap.setSwapRate(ADEL_AKRO_RATE, 1, {"from": deployer})
    cur_time = chain.time()
    chain.mine(1, cur_time)

    assert testVakroSwap.swapRateChangeTimestamp() == tx.timestamp

    cur_time = chain.time() + 100
    chain.mine(1, cur_time)

    testVakroSwap.setReverseSwapRate(ADEL_AKRO_RATE, 1, {"from": deployer})
    testVakroSwap.setStakingPool(stakingpool, {"from": deployer})
    testVakroSwap.setRewardStakingPool(NULL_ADDRESS, stakingpool, {"from": deployer})


def test_full_swap_with_reverse(
    chain, deployer, akro, adel, vakro, testVakroSwap, prepare_swap, regular_user
):
    cur_time = chain.time() + 100
    chain.mine(1, cur_time)

    assert vakro.balanceOf(regular_user) == 0
    assert adel.balanceOf(testVakroSwap.address) == 0

    ###
    # Swap
    ###
    adel_balance_before = adel.balanceOf(regular_user)

    assert testVakroSwap.adelSwapped(regular_user) == 0
    adel.approve(testVakroSwap.address, ADEL_TO_SWAP, {"from": regular_user})
    tx = testVakroSwap.swapFromAdel(
        ADEL_TO_SWAP, 0, ADEL_MAX_ALLOWED, [], {"from": regular_user}
    )

    users_time = tx.timestamp
    chain.mine(1, chain.time() + 100)

    # Check timestamps:
    assert testVakroSwap.swappedUsersTimestamps(regular_user) == users_time
    assert tx.timestamp > testVakroSwap.swapRateChangeTimestamp()

    # User has swapped ADEL and get vAkro. No new AKRO
    adel_balance_after = adel.balanceOf(regular_user)

    assert testVakroSwap.adelSwapped(regular_user) == ADEL_TO_SWAP
    assert adel_balance_before - adel_balance_after == ADEL_TO_SWAP
    assert vakro.balanceOf(regular_user) == ADEL_TO_SWAP * ADEL_AKRO_RATE
    assert adel.balanceOf(testVakroSwap.address) == ADEL_TO_SWAP

    # Reverse swap fails, because the user's timestamp is later than the rate change
    with brownie.reverts(revert_msg="User is not elligible for reverse swap"):
        testVakroSwap.swapReverseAdel({"from": regular_user})

    cur_time = chain.time() + 100
    chain.mine(1, cur_time)

    # Change rate, so the user will be able to swap in reverse
    tx = testVakroSwap.setSwapRate(ADEL_AKRO_RATE, 1, {"from": deployer})
    cur_time = tx.timestamp

    assert testVakroSwap.swapRateChangeTimestamp() == cur_time
    assert (
        testVakroSwap.swappedUsersTimestamps(regular_user) == users_time
    )  # not changed

    # Can reverse swap now
    testVakroSwap.swapReverseAdel({"from": regular_user})

    assert (
        adel.balanceOf(testVakroSwap.address) == 0
    )  # Because of the same reverse rate


def test_part_reverse_swap(
    chain, deployer, akro, adel, vakro, testVakroSwap, prepare_swap, regular_user2
):
    cur_time = chain.time() + 100
    chain.mine(1, cur_time)

    assert vakro.balanceOf(regular_user2) == 0
    assert adel.balanceOf(testVakroSwap.address) == 0

    ###
    # Swap
    ###
    adel_balance_before = adel.balanceOf(regular_user2)

    assert testVakroSwap.adelSwapped(regular_user2) == 0
    adel.approve(testVakroSwap.address, ADEL_TO_SWAP, {"from": regular_user2})
    tx = testVakroSwap.swapFromAdel(
        ADEL_TO_SWAP, 0, ADEL_MAX_ALLOWED, [], {"from": regular_user2}
    )

    users_time = tx.timestamp
    chain.mine(1, chain.time())
    chain.mine(1, chain.time() + 100)

    # Check timestamps:
    assert testVakroSwap.swappedUsersTimestamps(regular_user2) == users_time
    assert users_time > testVakroSwap.swapRateChangeTimestamp()

    # User has swapped ADEL and get vAkro. No new AKRO
    adel_balance_after = adel.balanceOf(regular_user2)

    assert testVakroSwap.adelSwapped(regular_user2) == ADEL_TO_SWAP
    assert adel_balance_before - adel_balance_after == ADEL_TO_SWAP
    assert vakro.balanceOf(regular_user2) == ADEL_TO_SWAP * ADEL_AKRO_RATE
    assert adel.balanceOf(testVakroSwap.address) == ADEL_TO_SWAP

    # Reverse swap fails, because the user's timestamp is later than the rate change
    with brownie.reverts(revert_msg="User is not elligible for reverse swap"):
        testVakroSwap.swapReverseAdel({"from": regular_user2})

    cur_time = chain.time() + 100
    chain.mine(1, cur_time)

    # Change rate, so the user will be able to swap in reverse
    tx = testVakroSwap.setSwapRate(ADEL_AKRO_RATE, 1, {"from": deployer})
    cur_time = tx.timestamp
    chain.mine(1, chain.time() + 100)

    # Provide additional swap
    adel.approve(testVakroSwap.address, ADEL_TO_SWAP, {"from": regular_user2})
    tx = testVakroSwap.swapFromAdel(
        ADEL_TO_SWAP, 0, ADEL_MAX_ALLOWED, [], {"from": regular_user2}
    )
    users_time2 = tx.timestamp
    chain.mine(1, chain.time() + 100)

    # Timestamp was updated
    assert testVakroSwap.swappedUsersTimestamps(regular_user2) == users_time2
    assert users_time2 > testVakroSwap.swapRateChangeTimestamp()

    # Cannot swap back

    # Reverse swap fails, because the user's timestamp is later than the rate change
    with brownie.reverts(revert_msg="User is not elligible for reverse swap"):
        testVakroSwap.swapReverseAdel({"from": regular_user2})
