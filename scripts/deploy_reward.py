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
        else:
            token_address_adel = os.getenv("TOKEN_FOR_REWARD_ADEL_MAINNET")
            token_address_akro = os.getenv("TOKEN_FOR_REWARD_AKRO_MAINNET")  
        # Admin is an account
        if admin_key:
            proxy_admin = accounts.add(admin_key)
        elif proxy_admin_address:  # Admin is a contract
            proxy_admin = get_proxy_admin(proxy_admin_address)
        else:  # New proxy admin needed
            proxy_admin = deploy_admin(deployer)
            print("ProxyAdmin deployed")

    print(f"You are using: 'deployer' [{deployer.address}]")
    print(f"Proxy Admin at {proxy_admin.address}")

    (reward_adel_contract_impl_from_proxy,reward_adel_proxy_contract,reward_adel_contract_impl)  = deploy_proxy(deployer, proxy_admin, Rewards, token_address_adel)
    (reward_akro_contract_impl_from_proxy,reward_akro_proxy_contract,reward_akro_contract_impl) = deploy_proxy(deployer, proxy_admin, Rewards, token_address_akro)
    print(f"Adel Rewards Implementation at {reward_adel_contract_impl_from_proxy}, Adel Rewards Proxy at {reward_adel_proxy_contract}, Adel Reward Contract Implementation at {reward_adel_contract_impl} with token {token_address_adel}")
    print(f"Akro Rewards Implementation at {reward_akro_contract_impl_from_proxy}, Akro Rewards Proxy at {reward_akro_proxy_contract}, Akro Reward Contract Implementation at {reward_akro_contract_impl} with token {token_address_akro}")
