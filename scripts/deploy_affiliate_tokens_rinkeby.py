import os
from dotenv import load_dotenv, find_dotenv
from brownie import *

from utils.deploy_helpers import deploy_proxy, deploy_admin, get_proxy_admin, upgrade_proxy



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


    # 1. Registry
    registry = deployer.deploy(TestRegistryV2)

    tokenUSDC = "0x4DBCdF9B62e891a7cec5A2568C3F4FAF9E8Abe2b"

    tokenDAI = "0x5592EC0cfb4dbc12D3aB100b257153436a1f0FEa"

    # 2. USDC Vault
    vaultUSDC = deployer.deploy(TestVaultV2)

    vaultUSDC.initialize(tokenUSDC, deployer, deployer, "", "", deployer, {"from":deployer})
    vaultUSDC.setDepositLimit(2 ** 256 - 1, {"from": deployer})

    registry.newRelease(vaultUSDC, {"from": deployer})
    registry.endorseVault(vaultUSDC, {"from": deployer})


    # 3. DAI Vault
    vaultDAI = deployer.deploy(TestVaultV2)

    vaultDAI.initialize(tokenDAI, deployer, deployer, "", "", deployer, {"from":deployer})
    vaultDAI.setDepositLimit(2 ** 256 - 1, {"from": deployer})

    registry.newRelease(vaultDAI, {"from": deployer})
    registry.endorseVault(vaultDAI, {"from": deployer})

    # 4. Affiliate token USDC Vault

    affiliateTokenImplFromProxy, affiliateTokenProxy, affiliateTokenImpl = deploy_proxy(
        affiliate, 
        proxy_admin, 
        AffiliateTokenUpgradeable,
        tokenUSDC,
        registry,
        f"AKRO - {tokenUSDC.symbol()} Vault",
        f"akrov{tokenUSDC.symbol()}")

    assert affiliateTokenProxy.admin.call({"from":proxy_admin.address}) == proxy_admin.address
    assert affiliateTokenProxy.implementation.call({"from":proxy_admin.address}) == affiliateTokenImpl.address

    print(f"AffiliateToken proxy deployed at {affiliateTokenImpl.address}")
    print(f"AffiliateToken implementation deployed at {affiliateTokenProxy.address}")

    # 5. Affiliate token DAI Vault

    affiliateTokenImplFromProxy, affiliateTokenProxy, affiliateTokenImpl = deploy_proxy(
        affiliate, 
        proxy_admin, 
        AffiliateTokenUpgradeable,
        tokenDAI,
        registry,
        f"AKRO - {tokenDAI.symbol()} Vault",
        f"akrov{tokenDAI.symbol()}")

    assert affiliateTokenProxy.admin.call({"from":proxy_admin.address}) == proxy_admin.address
    assert affiliateTokenProxy.implementation.call({"from":proxy_admin.address}) == affiliateTokenImpl.address

    print(f"AffiliateToken proxy deployed at {affiliateTokenImpl.address}")
    print(f"AffiliateToken implementation deployed at {affiliateTokenProxy.address}")


    
