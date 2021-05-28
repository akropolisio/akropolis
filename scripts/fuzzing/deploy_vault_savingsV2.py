import os
from dotenv import load_dotenv, find_dotenv
from brownie import *
#VaultSavings, yTestVault, TestERC20, YTestRegistry, YTestStrategy, accounts, network, web3

from utils.deploy_helpers import deploy_proxy, deploy_admin, get_proxy_admin, upgrade_proxy

HARVEY_ORIGIN = '0xAaaaAaAAaaaAAaAAaAaaaaAAAAAaAaaaAaAaaAA0'
HARVEY_ACCOUNT_1 = '0xAaAaaAAAaAaaAaAaAaaAAaAaAAAAAaAAAaaAaAa2'
HARVEY_ACCOUNT_2 = '0xafFEaFFEAFfeAfFEAffeaFfEAfFEaffeafFeAFfE'

def main():
    #load_dotenv(dotenv_path=Path('..')/".env", override=True)
        
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


    # 1. 3Crv vault
    token_3Crv = deployer.deploy(PoolTokenV1_3Crv)
    print(f"Token deployed at {token_3Crv.address}")

    yVault_3Crv = deployer.deploy(TestVaultV2)
    yVault_3Crv.initialize(token_3Crv.address, deployer.address, deployer.address, "", "", {"from": deployer})
    yVault_3Crv.setGovernance(deployer.address, {"from": deployer})
    yVault_3Crv.setRewards(deployer.address, {"from": deployer})
    yVault_3Crv.setGuardian(deployer.address, {"from": deployer})
    yVault_3Crv.setDepositLimit(2 ** 256 - 1, {"from": deployer})
    yVault_3Crv.setManagementFee(0, {"from": deployer})
    print(f"3Crv Vault deployed at {yVault_3Crv.address}")

    strategy_3crv = deployer.deploy(StubStrategyV2, yVault_3Crv.address, deployer.address, 200)
    token_3Crv.approve(strategy_3crv.address, 10**18, {"from":deployer})
    strategy_3crv.setKeeper(deployer, {"from": deployer})
    print(f"Strategy deployed at {strategy_3crv.address}")
    

    #Deploy VaultSavings, Registry and add Vaults
    vaultSavingsImplFromProxy, vaultSavingsProxy, vaultSavingsImpl = deploy_proxy(deployer, proxy_admin, VaultSavingsV2)
    print(f"VaultSavings proxy deployed at {vaultSavingsImpl.address}")
    print(f"VaultSavings implementation deployed at {vaultSavingsProxy.address}")

    registry = deployer.deploy(TestRegistryV2)
    registry.setGovernance(deployer,  {"from": deployer})
    print(f"Registry deployed at {registry.address}")

   
    registry.newRelease(yVault_3Crv.address, {'from': deployer})
    vaultSavingsImplFromProxy.registerVault.transact(yVault_3Crv.address, {'from': deployer})
    print("crvCOMP Vault registered")

    yVault_3Crv.setGovernance(HARVEY_ORIGIN, {"from": deployer})
    yVault_3Crv.setRewards(HARVEY_ORIGIN, {"from": deployer})
    yVault_3Crv.setGuardian(HARVEY_ORIGIN, {"from": deployer})
    strategy_3crv.setKeeper(HARVEY_ORIGIN, {"from": deployer})

    vaultSavingsImplFromProxy.transferOwnership.transact(HARVEY_ORIGIN, {'from': deployer})
