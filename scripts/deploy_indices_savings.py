import os
from dotenv import load_dotenv, find_dotenv
from brownie import *
#IndicesSavings, HelperWETH, accounts, network, web3

from utils.deploy_helpers import deploy_proxy, deploy_admin, get_proxy_admin, upgrade_proxy

MAINNET_NETWORK_ID = 1

def sushi_router():
    if network.chain.id == MAINNET_NETWORK_ID:
        return os.getenv("MAINNET_SUSHI_ROUTER")
    raise "unknown network"

def PIPT():
    if network.chain.id == MAINNET_NETWORK_ID:
        return os.getenv("MAINNET_PIPT")
    raise "unknown network"

def YETI():
    if network.chain.id == MAINNET_NETWORK_ID:
        return os.getenv("MAINNET_YETI")
    raise "unknown network"

def ASSY():
    if network.chain.id == MAINNET_NETWORK_ID:
        return os.getenv("MAINNET_ASSY")
    raise "unknown network"

def YLA():
    if network.chain.id == MAINNET_NETWORK_ID:
        return os.getenv("MAINNET_YLA")
    raise "unknown network"

def main():
    load_dotenv(dotenv_path="./.env", override=True)
        
    load_dotenv(find_dotenv())

    print(f"You are using the '{network.show_active()}' network")
    if (network.show_active() == 'development'):
        deployer = accounts[0]
        proxy_admin = accounts[1]
    else:
        deployer = accounts.add(os.getenv("DEPLOYER_PRIVATE_KEY"))
        admin_key = os.getenv("ADMIN_PRIVATE_KEY")
        proxy_admin_address = os.getenv("PROXY_ADMIN_ADDRESS")
        # Admin is an account
        if admin_key:
            proxy_admin = accounts.add(admin_key)
        elif proxy_admin_address: #Admin is a contract
            proxy_admin = get_proxy_admin(proxy_admin_address)
        else: #New proxy admin needed
            proxy_admin = deploy_admin(deployer)
            print("ProxyAdmin deployed")

    print(f"You are using: 'deployer' [{deployer.address}]")
    print(f"Proxy Admin at {proxy_admin.address}")

    # Contract for swap WETH to ETH
    helperWETH = deployer.deploy(HelperWETH)

    #Deploy IndicesSavings
    indicesSavingsImplFromProxy, indicesSavingsProxy, indicesSavingsImpl = deploy_proxy(deployer, proxy_admin, IndicesSavings, helperWETH.address)
    print(f"IndicesSavings proxy deployed at {indicesSavingsImpl.address}")
    print(f"IndicesSavings implementation deployed at {indicesSavingsProxy.address}")

    #Register indices
    indicesSavingsImplFromProxy.registerIndex.transact(PIPT(), sushi_router(), {'from': deployer})
    indicesSavingsImplFromProxy.registerIndex.transact(YETI(), sushi_router(), {'from': deployer})
    indicesSavingsImplFromProxy.registerIndex.transact(ASSY(), sushi_router(), {'from': deployer})
    indicesSavingsImplFromProxy.registerIndex.transact(YLA(), sushi_router(), {'from': deployer})

