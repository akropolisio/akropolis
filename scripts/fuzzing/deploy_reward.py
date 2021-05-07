import os
from dotenv import load_dotenv, find_dotenv
from brownie import *
from web3 import Web3
#Rewards, accounts, network, web3

from utils.deploy_helpers import deploy_proxy, deploy_admin, get_proxy_admin, upgrade_proxy

HARVEY_ORIGIN = '0xAaaaAaAAaaaAAaAAaAaaaaAAAAAaAaaaAaAaaAA0'
HARVEY_ACCOUNT_1 = '0xAaAaaAAAaAaaAaAaAaaAAaAaAAAAAaAAAaaAaAa2'
HARVEY_ACCOUNT_2 = '0xafFEaFFEAFfeAfFEAffeaFfEAfFEaffeafFeAFfE'

NULL_ADDRESS = '0x0000000000000000000000000000000000000000'
AVAILABLE_USER1 = 2000
AVAILABLE_USER2 = 4000
AVAILABLE_USER3 = 1500
AVAILABLE_USER4 = 2500
FULL_BALANCE_IN_SNAPSHOT = 10000

def prepare_deployer():
    return accounts[0]
def regular_user(accounts):
    return accounts[1]
def regular_user2(accounts):
    return accounts[2]
def regular_user3(accounts):
    return accounts[3]
def regular_user4(accounts):
    return accounts[4]

def proxy_admin(deployer):
    proxy_admin = deploy_admin(deployer)
    return proxy_admin

def prepare_token(deployer, TestERC20):
    token = deployer.deploy(TestERC20, "token", "TKN", 18)
    token.mint.transact(1500000000, {"from": deployer})
    return token

def prepare_rewards(deployer, proxy_admin, token, Rewards):
    rewardsImplFromProxy, rewardsProxy, rewardsImpl = deploy_proxy(deployer, proxy_admin, Rewards, token.address)

    assert rewardsProxy.admin.call({"from":proxy_admin.address}) == proxy_admin.address
    assert rewardsProxy.implementation.call({"from":proxy_admin.address}) == rewardsImpl.address

    return rewardsImplFromProxy

def to_keccak(types, str):
    return Web3.solidityKeccak(types, str)

def prepare_root(users, values):
    h1 = to_keccak( ['address', 'uint256'], [str(users[0]), values[0]] )
    h2 = to_keccak( ['address', 'uint256'], [str(users[1]), values[1]] )
    h3 = to_keccak( ['address', 'uint256'], [str(users[2]), values[2]] )
    h4 = to_keccak( ['address', 'uint256'], [str(users[3]), values[3]] )

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

def prepare_claim_reward(deployer, rewards, token, regular_user, regular_user2, regular_user3, regular_user4):
    users = [regular_user, regular_user2, regular_user3, regular_user4]
    values = [AVAILABLE_USER1, AVAILABLE_USER2, AVAILABLE_USER3, AVAILABLE_USER4]
    root, hshs = prepare_root(users, values)
    h1, h2, h3, h4, root_1, root_2 = hshs

    rewards.setMerkleRoots.transact([root], {'from': deployer})
    token.transfer.transact(rewards.address, FULL_BALANCE_IN_SNAPSHOT, {'from': deployer})

    # if nead claim uncoment next line
    #rewards.claim.transact(0, AVAILABLE_USER1, [h2, root_2], {'from': regular_user})

def main():
    deployer = prepare_deployer()
    token = prepare_token(deployer, TestERC20)

    rewards = prepare_rewards(deployer, proxy_admin(deployer), token, Rewards)
    prepare_claim_reward(deployer, rewards,token, regular_user(accounts), regular_user2(accounts), regular_user3(accounts), regular_user4(accounts))

    rewards.transferOwnership.transact(HARVEY_ORIGIN, {'from': deployer})

