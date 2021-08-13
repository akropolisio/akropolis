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
    # load_dotenv(dotenv_path=Path('..')/".env", override=True)

    load_dotenv(find_dotenv())

    print(f"You are using the '{network.show_active()}' network")
    if network.show_active() == "development":
        deployer = accounts[0]
        proxy_admin = accounts[1]
    else:
        deployer = accounts.add(os.getenv("DEPLOYER_PRIVATE_KEY"))
        admin_key = os.getenv("ADMIN_PRIVATE_KEY")
        proxy_admin_address = os.getenv("PROXY_ADMIN_ADDRESS")
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

    token_address = os.getenv("TOKEN_FOR_REWARD")

    reward = deployer.deploy(Rewards)
    reward.initialize(token_address, {"from": deployer})
    print(f"Rewards at {reward.address} with token {token_address}")
