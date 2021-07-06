import pytest
import brownie
from web3 import Web3

ADEL_TO_SWAP = 100
AKRO_ON_SWAP = 10000
ADEL_AKRO_RATE = 15
EPOCH_LENGTH = 100
REWARDS_AMOUNT = 150
ADEL_MAX_ALLOWED = 1000
NULL_ADDRESS = '0x0000000000000000000000000000000000000000'
AVAILABLE_USER1 = 2000
AVAILABLE_USER2 = 4000
AVAILABLE_USER3 = 1500
AVAILABLE_USER4 = 2500
ADEL_TO_STAKE = 500
ADEL_TO_RECEIVE_BACK = 300
ADEL_TO_SWAP_USER1 = AVAILABLE_USER1 - 200



@pytest.fixture(scope="module")
def prepare_swap(deployer, adel, akro, vakro, stakingpool, vakroSwap, exploitCompVAkroSwap):
    vakro.addMinter(vakroSwap.address, {'from': deployer})
    vakro.addSender(vakroSwap.address, {'from': deployer})
    vakro.addMinter(exploitCompVAkroSwap.address, {'from': deployer})
    vakro.addSender(exploitCompVAkroSwap.address, {'from': deployer})

    adel.addMinter(vakroSwap.address, {'from': deployer})

    stakingpool.setSwapContract(vakroSwap.address, {'from': deployer})

    vakroSwap.setSwapRate(ADEL_AKRO_RATE, 1, {'from': deployer})
    vakroSwap.setStakingPool(stakingpool, {'from': deployer})
    vakroSwap.setRewardStakingPool(NULL_ADDRESS, stakingpool, {'from': deployer})

def encode(s):
    return s.encode("utf-8")

def hexify(s):
    return encode(s).hex()

def to_keccak(types, str):
    return Web3.solidityKeccak(types, str)

def prepare_root(regular_user, regular_user2, regular_user3, regular_user4):
    h1 = to_keccak( ['address', 'uint256'], [regular_user, AVAILABLE_USER1] )
    h2 = to_keccak( ['address', 'uint256'], [regular_user2, AVAILABLE_USER2] )

    h3 = to_keccak( ['address', 'uint256'], [regular_user3, AVAILABLE_USER3] )
    h4 = to_keccak( ['address', 'uint256'], [regular_user4, AVAILABLE_USER4] )

    root_1 = ''
    root_2 = ''
    root = ''
    if int(h1.hex(), 16) <= int(h2.hex(), 16):
        root_1 = to_keccak(['bytes32', 'bytes32'], [h1, h2] )
    else:
        root_1 = to_keccak(['bytes32', 'bytes32'], [h2, h1] )

    if int(h3.hex(), 16) <= int(h4.hex(), 16):
        root_2 = to_keccak(['bytes32', 'bytes32'], [h3, h4] )
    else:
        root_2 = to_keccak(['bytes32', 'bytes32'], [h4, h3] )

    if int(root_1.hex(), 16) <= int(root_2.hex(), 16):
        root = to_keccak(['bytes32', 'bytes32'], [root_1, root_2] )
    else:
        root = to_keccak(['bytes32', 'bytes32'], [root_2, root_1] )
    return (root, [h1, h2, h3, h4, root_1, root_2])



def test_swap_adel(chain, deployer, akro, adel, vakro, stakingpool, vakroSwap, prepare_swap, regular_user, regular_user2, regular_user3, regular_user4):
    root, hshs = prepare_root(regular_user.address, regular_user2.address, regular_user3.address, regular_user4.address)

    h1, h2, h3, h4, root_1, root_2 = hshs


    # Set root and settings
    vakroSwap.setMerkleRoots([root], {'from': deployer})
    vakro.setVestingCliff(0, {'from': deployer})
    start = chain.time() + 50
    vakro.setVestingStart(start, {'from': deployer})
    chain.mine(1)

    # Add stake
    adel.approve(stakingpool.address, ADEL_TO_STAKE, {'from': regular_user})
    stakingpool.stake(ADEL_TO_STAKE, hexify("Some string"), {'from': regular_user}) 
    
    ###
    # Swap enough Adel to reach almost max available
    ###
    adel.approve(vakroSwap.address, ADEL_TO_SWAP_USER1, {'from': regular_user})
    vakroSwap.swapFromAdel(ADEL_TO_SWAP_USER1, 0, AVAILABLE_USER1, [h2, root_2], {'from': regular_user})
    assert vakroSwap.adelSwapped(regular_user) == ADEL_TO_SWAP_USER1

    ###
    # Unstake Adel tokens left and get the change
    ###
    chain.mine(1, start + EPOCH_LENGTH)

    adel_balance_before = adel.balanceOf(regular_user)
    vakroSwap.swapFromStakedAdel(0, AVAILABLE_USER1, [h2, root_2], {'from': regular_user})
    adel_balance_after = adel.balanceOf(regular_user)

    # Max achieved
    assert vakroSwap.adelSwapped(regular_user) == AVAILABLE_USER1

    # Change receive
    assert adel_balance_after - adel_balance_before == ADEL_TO_RECEIVE_BACK

    # No extra Adel collected
    assert adel.balanceOf(vakroSwap.address) == AVAILABLE_USER1



def test_swap_exploit_comp_vakro(chain, deployer, vakro, exploitCompVAkroSwap, prepare_swap, regular_user, regular_user2, regular_user3, regular_user4):
    root, hshs = prepare_root(regular_user.address, regular_user2.address, regular_user3.address, regular_user4.address)

    h1, h2, h3, h4, root_1, root_2 = hshs

    # Set root and settings
    exploitCompVAkroSwap.setMerkleRoots([root], {'from': deployer})
    vakro.setVestingCliff(0, {'from': deployer})
    start = chain.time() + 50
    vakro.setVestingStart(start, {'from': deployer})
    chain.mine(1)

    exploitCompVAkroSwap.swap(0, AVAILABLE_USER1, [h2, root_2], {'from': regular_user})
    assert exploitCompVAkroSwap.swapped(regular_user) == AVAILABLE_USER1
