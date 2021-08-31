import os
from dotenv import load_dotenv, find_dotenv
from brownie import *

# Rewards, accounts, network, web3

from utils.deploy_helpers import (
    deploy_proxy,
    deploy_admin,
    get_proxy_admin,
    upgrade_proxy,
)


def main():
    load_dotenv(find_dotenv())

    print(f"You are using the '{network.show_active()}' network")
    if network.show_active() == "development":
        deployer = accounts[0]
        proxy_admin = accounts[1]
    else:
        deployer = accounts.add(os.getenv("DEPLOYER_PRIVATE_KEY"))
        admin_key = os.getenv("ADMIN_PRIVATE_KEY")
        proxy_admin_address = os.getenv("PROXY_ADMIN_ADDRESS")
        if  network.show_active() == "rinkeby":
            token_address_adel = os.getenv("TOKEN_FOR_REWARD_ADEL_RINKEBY")
            token_address_akro = os.getenv("TOKEN_FOR_REWARD_AKRO_RINKEBY")
            merkle_root_adel = os.getenv("MERKLE_ROOT_ADEL_RINKEBY")
            merkle_root_akro = os.getenv("MERKLE_ROOT_AKRO_RINKEBY")
        else:
            token_address_adel = os.getenv("TOKEN_FOR_REWARD_ADEL_MAINNET")
            token_address_akro = os.getenv("TOKEN_FOR_REWARD_AKRO_MAINNET")
            merkle_root_adel = os.getenv("MERKLE_ROOT_AKRO_MAINNET")
            merkle_root_akro = os.getenv("MERKLE_ROOT_AKRO_MAINNET")      
        # Admin is an account
        if admin_key:
            proxy_admin = accounts.add(admin_key)
        elif proxy_admin_address:  # Admin is a contract
            proxy_admin = get_proxy_admin(proxy_admin_address)
        else:  # New proxy admin needed
            proxy_admin = deploy_admin(deployer)
            print("ProxyAdmin deployed")
            # proxy_admin = (project.get_loaded_projects()[0]).UtilProxyAdmin


    print(f"You are using: 'deployer' [{deployer.address}]")
    print(f"Proxy Admin at {proxy_admin.address}")
    # print(f"Projects object is {(project.get_loaded_projects()[0]).__dict__}")


# contract_impl_from_proxy, proxy_contract, contract_impl
#     # reward_adel = deployer.deploy(Rewards)
#     # reward_akro = deployer.deploy(Rewards)
    reward_adel = deploy_proxy(deployer, proxy_admin, Rewards, token_address_adel)
    reward_akro = deploy_proxy(deployer, proxy_admin, Rewards, token_address_akro)
    # reward_adel_proxy = deployer.deploy_proxy(reward_adel.address, proxy_admin.address,{"from": deployer, "gas_limit": 1000000},)
    # reward_akro_proxy = deployer.deploy_proxy(reward_akro.address, proxy_admin.address, {"from": deployer, "gas_limit": 1000000},)
    # reward_adel.initialize(token_address_adel, {"from": proxy_admin})
    # reward_akro.initialize(token_address_akro, {"from": proxy_admin})
    print(f"Adel Rewards Implementation at {reward_adel.contract_impl_from_proxy}, Adel Rewards Proxy at {reward_adel.proxy_contract}, Adel Reward Contract Implementation at {reward_adel.contract_impl} with token {token_address_adel}")
    print(f"Adel Rewards Implementation at {reward_akro.contract_impl_from_proxy}, Adel Rewards Proxy at {reward_akro.proxy_contract}, Adel Reward Contract Implementation at {reward_akro.contract_impl} with token {token_address_adel}")
    # print(f"Akro Rewards at {reward_akro.address} with token {token_address_akro}")
    # print(f"Adel Rewards Proxy at {reward_adel_proxy} ")
    # print(f"Akro Rewards Proxy at {reward_akro_proxy} ")

    # reward_adel.setMerkleRoots(merkle_root_adel, {"from": deployer})
    # reward_adel.setMerkleRoots(merkle_root_akro, {"from": deployer})

def retrieve_proxy_admin():
    cur_project = project.get_loaded_projects()[0]
    return Contract.from_abi(
        cur_project.UtilProxyAdmin._name,
        proxy_admin_address,
        cur_project.UtilProxyAdmin.abi,
        )
