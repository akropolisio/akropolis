import pytest
import brownie
from web3 import Web3

NULL_ADDRESS = "0x0000000000000000000000000000000000000000"
AVAILABLE_USER1 = 2000
AVAILABLE_USER2 = 4000
AVAILABLE_USER3 = 1500
AVAILABLE_USER4 = 2500
FULL_BALANCE_IN_SNAPSHOT = 10000


def to_keccak(types, str):
    return Web3.solidityKeccak(types, str)


def prepare_root(users, values):
    h1 = to_keccak(["address", "uint256"], [str(users[0]), values[0]])
    h2 = to_keccak(["address", "uint256"], [str(users[1]), values[1]])
    h3 = to_keccak(["address", "uint256"], [str(users[2]), values[2]])
    h4 = to_keccak(["address", "uint256"], [str(users[3]), values[3]])

    root_1 = ""
    root_2 = ""
    root = ""
    if int(h1.hex(), 16) <= int(h2.hex(), 16):
        root_1 = to_keccak(["bytes32", "bytes32"], [h1, h2])
    else:
        root_1 = to_keccak(["bytes32", "bytes32"], [h2, h1])

    if int(h3.hex(), 16) <= int(h4.hex(), 16):
        root_2 = to_keccak(["bytes32", "bytes32"], [h3, h4])
    else:
        root_2 = to_keccak(["bytes32", "bytes32"], [h4, h3])

    if int(root_1.hex(), 16) <= int(root_2.hex(), 16):
        root = to_keccak(["bytes32", "bytes32"], [root_1, root_2])
    else:
        root = to_keccak(["bytes32", "bytes32"], [root_2, root_1])
    return (root, [h1, h2, h3, h4, root_1, root_2])


def test_successful_claim_reward(
    deployer, rewards, token, regular_user, regular_user2, regular_user3, regular_user4
):
    users = [regular_user, regular_user2, regular_user3, regular_user4]
    values = [AVAILABLE_USER1, AVAILABLE_USER2, AVAILABLE_USER3, AVAILABLE_USER4]
    root, hshs = prepare_root(users, values)
    h1, h2, h3, h4, root_1, root_2 = hshs

    # Set root and settings
    rewards.setMerkleRoots([root], {"from": deployer})
    token.transfer(rewards.address, FULL_BALANCE_IN_SNAPSHOT, {"from": deployer})

    token_balance_before = token.balanceOf(regular_user)
    rewards.claim(0, AVAILABLE_USER1, [h2, root_2], {"from": regular_user})
    token_balance_after = token.balanceOf(regular_user)
    assert token_balance_after - token_balance_before == AVAILABLE_USER1


def test_wrong_leaf(
    deployer, rewards, token, regular_user, regular_user2, regular_user3, regular_user4
):
    users = [regular_user, regular_user2, regular_user3, regular_user4]
    values = [AVAILABLE_USER1, AVAILABLE_USER2, AVAILABLE_USER3, AVAILABLE_USER4]
    root, hshs = prepare_root(users, values)
    h1, h2, h3, h4, root_1, root_2 = hshs

    # Set root and settings
    rewards.setMerkleRoots([root], {"from": deployer})
    token.transfer(rewards.address, FULL_BALANCE_IN_SNAPSHOT, {"from": deployer})

    with brownie.reverts(revert_pattern="Merkle proofs not verified"):
        rewards.claim(0, AVAILABLE_USER1, [h3, root_2], {"from": regular_user})


def test_successful_claim_new_part(
    deployer, rewards, token, regular_user, regular_user2, regular_user3, regular_user4
):
    users = [regular_user, regular_user2, regular_user3, regular_user4]
    values = [AVAILABLE_USER1, AVAILABLE_USER2, AVAILABLE_USER3, AVAILABLE_USER4]
    root, hshs = prepare_root(users, values)
    h1, h2, h3, h4, root_1, root_2 = hshs

    # Set root and settings
    rewards.setMerkleRoots([root], {"from": deployer})
    token.transfer(rewards.address, FULL_BALANCE_IN_SNAPSHOT, {"from": deployer})

    token_balance_before = token.balanceOf(regular_user)
    rewards.claim(0, AVAILABLE_USER1, [h2, root_2], {"from": regular_user})
    token_balance_after = token.balanceOf(regular_user)
    assert token_balance_after - token_balance_before == AVAILABLE_USER1

    AVAILABLE_USER1_TOTAL = AVAILABLE_USER1 * 2
    users = [regular_user, regular_user2, regular_user3, regular_user4]
    values = [AVAILABLE_USER1_TOTAL, AVAILABLE_USER2, AVAILABLE_USER3, AVAILABLE_USER4]
    root, hshs = prepare_root(users, values)
    h1, h2, h3, h4, root_1, root_2 = hshs

    # update root and settings
    rewards.setMerkleRoots([root], {"from": deployer})
    token.transfer(rewards.address, FULL_BALANCE_IN_SNAPSHOT, {"from": deployer})

    token_balance_before = token.balanceOf(regular_user)
    rewards.claim(0, AVAILABLE_USER1_TOTAL, [h2, root_2], {"from": regular_user})
    token_balance_after = token.balanceOf(regular_user)
    assert token_balance_after - token_balance_before == AVAILABLE_USER1


def test_claim_reward_over(
    deployer, rewards, token, regular_user, regular_user2, regular_user3, regular_user4
):
    users = [regular_user, regular_user2, regular_user3, regular_user4]
    values = [AVAILABLE_USER1, AVAILABLE_USER2, AVAILABLE_USER3, AVAILABLE_USER4]
    root, hshs = prepare_root(users, values)
    h1, h2, h3, h4, root_1, root_2 = hshs

    # Set root and settings
    rewards.setMerkleRoots([root], {"from": deployer})
    token.transfer(rewards.address, FULL_BALANCE_IN_SNAPSHOT, {"from": deployer})

    token_balance_before = token.balanceOf(regular_user)
    rewards.claim(0, AVAILABLE_USER1, [h2, root_2], {"from": regular_user})
    token_balance_after = token.balanceOf(regular_user)
    assert token_balance_after - token_balance_before == AVAILABLE_USER1

    token_balance_before = token.balanceOf(regular_user)
    with brownie.reverts(revert_pattern="Merkle proofs not verified"):
        rewards.claim(0, AVAILABLE_USER1, [h3, root_2], {"from": regular_user})
    token_balance_after = token.balanceOf(regular_user)
    assert token_balance_after - token_balance_before == 0


def test_claim_reward_from_empty_pool(
    deployer, rewards, token, regular_user, regular_user2, regular_user3, regular_user4
):
    users = [regular_user, regular_user2, regular_user3, regular_user4]
    values = [AVAILABLE_USER1, AVAILABLE_USER2, AVAILABLE_USER3, AVAILABLE_USER4]
    root, hshs = prepare_root(users, values)
    h1, h2, h3, h4, root_1, root_2 = hshs

    # Set root and settings
    rewards.setMerkleRoots([root], {"from": deployer})
    # small balance in Rewards contract
    token.transfer(rewards.address, AVAILABLE_USER1 / 2, {"from": deployer})

    token_balance_before = token.balanceOf(regular_user)
    with brownie.reverts():
        rewards.claim(0, AVAILABLE_USER1, [h3, root_2], {"from": regular_user})
    token_balance_after = token.balanceOf(regular_user)
    assert token_balance_after - token_balance_before == 0


def test_claim_reward_with_wrong_index(
    deployer, rewards, token, regular_user, regular_user2, regular_user3, regular_user4
):
    users = [regular_user, regular_user2, regular_user3, regular_user4]
    values = [AVAILABLE_USER1, AVAILABLE_USER2, AVAILABLE_USER3, AVAILABLE_USER4]
    root, hshs = prepare_root(users, values)
    h1, h2, h3, h4, root_1, root_2 = hshs

    # Set root and settings
    rewards.setMerkleRoots([root], {"from": deployer})
    token.transfer(rewards.address, AVAILABLE_USER1, {"from": deployer})

    token_balance_before = token.balanceOf(regular_user)
    with brownie.reverts():
        rewards.claim(123, AVAILABLE_USER1, [h3, root_2], {"from": regular_user})
    token_balance_after = token.balanceOf(regular_user)
    assert token_balance_after - token_balance_before == 0


def test_min_claim_amount(
    deployer, rewards, token, regular_user, regular_user2, regular_user3, regular_user4
):
    users = [regular_user, regular_user2, regular_user3, regular_user4]
    values = [AVAILABLE_USER1, AVAILABLE_USER2, AVAILABLE_USER3, AVAILABLE_USER4]
    root, hshs = prepare_root(users, values)
    h1, h2, h3, h4, root_1, root_2 = hshs

    # Set root and settings
    rewards.setMerkleRoots([root], {"from": deployer})
    token.transfer(rewards.address, FULL_BALANCE_IN_SNAPSHOT, {"from": deployer})

    MINIMUM_CLAIM_AMOUNT = AVAILABLE_USER1 * 2
    rewards.setMinClaimAmount(MINIMUM_CLAIM_AMOUNT, {"from": deployer})

    token_balance_before = token.balanceOf(regular_user)
    with brownie.reverts():
        rewards.claim(0, AVAILABLE_USER1, [h3, root_2], {"from": regular_user})
    token_balance_after = token.balanceOf(regular_user)
    assert token_balance_after - token_balance_before == 0

    users = [regular_user, regular_user2, regular_user3, regular_user4]
    values = [MINIMUM_CLAIM_AMOUNT, AVAILABLE_USER2, AVAILABLE_USER3, AVAILABLE_USER4]
    root, hshs = prepare_root(users, values)
    h1, h2, h3, h4, root_1, root_2 = hshs

    # update root and settings
    rewards.setMerkleRoots([root], {"from": deployer})
    token.transfer(rewards.address, FULL_BALANCE_IN_SNAPSHOT, {"from": deployer})

    token_balance_before = token.balanceOf(regular_user)
    rewards.claim(0, MINIMUM_CLAIM_AMOUNT, [h2, root_2], {"from": regular_user})
    token_balance_after = token.balanceOf(regular_user)
    assert token_balance_after - token_balance_before == MINIMUM_CLAIM_AMOUNT


def test_min_claim_amount_access(deployer, rewards, regular_user):
    with brownie.reverts():
        rewards.setMinClaimAmount(123456, {"from": regular_user})


def test_pause_and_unpause_access(deployer, rewards, regular_user):
    with brownie.reverts():
        rewards.pause({"from": regular_user})
    with brownie.reverts():
        rewards.pause({"from": deployer})
        rewards.unpause({"from": regular_user})


def test_claim_reward_on_pause(
    deployer, rewards, token, regular_user, regular_user2, regular_user3, regular_user4
):
    users = [regular_user, regular_user2, regular_user3, regular_user4]
    values = [AVAILABLE_USER1, AVAILABLE_USER2, AVAILABLE_USER3, AVAILABLE_USER4]
    root, hshs = prepare_root(users, values)
    h1, h2, h3, h4, root_1, root_2 = hshs

    # Set root and settings
    rewards.setMerkleRoots([root], {"from": deployer})
    token.transfer(rewards.address, FULL_BALANCE_IN_SNAPSHOT, {"from": deployer})

    rewards.pause({"from": deployer})

    token_balance_before = token.balanceOf(regular_user)
    with brownie.reverts():
        rewards.claim(0, AVAILABLE_USER1, [h2, root_2], {"from": regular_user})
    token_balance_after = token.balanceOf(regular_user)
    assert token_balance_after - token_balance_before == 0

    rewards.unpause({"from": deployer})

    token_balance_before = token.balanceOf(regular_user)
    rewards.claim(0, AVAILABLE_USER1, [h2, root_2], {"from": regular_user})
    token_balance_after = token.balanceOf(regular_user)
    assert token_balance_after - token_balance_before == AVAILABLE_USER1


def test_withdraw_token(deployer, rewards, token, regular_user):
    token.transfer(rewards.address, FULL_BALANCE_IN_SNAPSHOT, {"from": deployer})

    token_balance_before = token.balanceOf(regular_user)
    with brownie.reverts():
        rewards.withdrawToken(regular_user, {"from": regular_user})
    token_balance_after = token.balanceOf(regular_user)
    assert token_balance_after - token_balance_before == 0

    token_balance_before = token.balanceOf(regular_user)
    rewards.withdrawToken(regular_user, {"from": deployer})
    token_balance_after = token.balanceOf(regular_user)
    assert token_balance_after - token_balance_before == FULL_BALANCE_IN_SNAPSHOT
