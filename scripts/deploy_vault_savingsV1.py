import os
from dotenv import load_dotenv, find_dotenv
from brownie import *

# VaultSavings, yTestVault, TestERC20, YTestRegistry, YTestController, YTestStrategy, accounts, network, web3

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

    # Deploy controller
    controller = deployer.deploy(YTestController, deployer.address)
    print(f"Controller deployed at {controller.address}")

    # 1. 3Crv vault
    token_3Crv = deployer.deploy(PoolTokenV1_3Crv)
    print(f"Token deployed at {token_3Crv.address}")

    yVault_3Crv = deployer.deploy(yTestVault, token_3Crv.address, controller.address)
    print(f"3Crv Vault deployed at {yVault_3Crv.address}")

    strategy_3crv = deployer.deploy(YTestStrategy, token_3Crv.address)
    print(f"Strategy deployed at {strategy_3crv.address}")

    controller.setVault(token_3Crv.address, yVault_3Crv.address, {"from": deployer})
    controller.approveStrategy(
        token_3Crv.address, strategy_3crv.address, {"from": deployer}
    )
    controller.setStrategy(
        token_3Crv.address, strategy_3crv.address, {"from": deployer}
    )

    # 2. crvBUSD vault
    token_crvBUSD = deployer.deploy(PoolTokenV1_crvBUSD)
    print(f"Token deployed at {token_crvBUSD.address}")

    yVault_crvBUSD = deployer.deploy(
        yTestVault, token_crvBUSD.address, controller.address
    )
    print(f"crvBUSD Vault deployed at {yVault_crvBUSD.address}")

    strategy_crvBUSD = deployer.deploy(YTestStrategy, token_crvBUSD.address)
    print(f"Strategy deployed at {strategy_crvBUSD.address}")

    controller.setVault(
        token_crvBUSD.address, yVault_crvBUSD.address, {"from": deployer}
    )
    controller.approveStrategy(
        token_crvBUSD.address, strategy_crvBUSD.address, {"from": deployer}
    )
    controller.setStrategy(
        token_crvBUSD.address, strategy_crvBUSD.address, {"from": deployer}
    )

    # 3. yUSD vault
    token_yUSD = deployer.deploy(PoolTokenV1_yUSD)
    print(f"yUSD deployed at {token_yUSD.address}")

    yVault_yUSD = deployer.deploy(yTestVault, token_yUSD.address, controller.address)
    print(f"yUSD Vault deployed at {yVault_yUSD.address}")

    strategy_yUSD = deployer.deploy(YTestStrategy, token_yUSD.address)
    print(f"Strategy deployed at {strategy_yUSD.address}")

    controller.setVault(token_yUSD.address, yVault_yUSD.address, {"from": deployer})
    controller.approveStrategy(
        token_yUSD.address, strategy_yUSD.address, {"from": deployer}
    )
    controller.setStrategy(
        token_yUSD.address, strategy_yUSD.address, {"from": deployer}
    )

    # 4. SBTC vault
    token_SBTC = deployer.deploy(PoolTokenV1_SBTC)
    print(f"Token deployed at {token_SBTC.address}")

    yVault_SBTC = deployer.deploy(yTestVault, token_SBTC.address, controller.address)
    print(f"SBTC Vault deployed at {yVault_SBTC.address}")

    strategy_SBTC = deployer.deploy(YTestStrategy, token_SBTC.address)
    print(f"Strategy deployed at {strategy_SBTC.address}")

    controller.setVault(token_SBTC.address, yVault_SBTC.address, {"from": deployer})
    controller.approveStrategy(
        token_SBTC.address, strategy_SBTC.address, {"from": deployer}
    )
    controller.setStrategy(
        token_SBTC.address, strategy_SBTC.address, {"from": deployer}
    )

    # 4. crvCOMP vault
    token_crvCOMP = deployer.deploy(PoolTokenV1_crvCOMP)
    print(f"Token deployed at {token_crvCOMP.address}")

    yVault_crvCOMP = deployer.deploy(
        yTestVault, token_crvCOMP.address, controller.address
    )
    print(f"crvCOMP Vault deployed at {yVault_crvCOMP.address}")

    strategy_crvCOMP = deployer.deploy(YTestStrategy, token_crvCOMP.address)
    print(f"Strategy deployed at {strategy_crvCOMP.address}")

    controller.setVault(
        token_crvCOMP.address, yVault_crvCOMP.address, {"from": deployer}
    )
    controller.approveStrategy(
        token_crvCOMP.address, strategy_crvCOMP.address, {"from": deployer}
    )
    controller.setStrategy(
        token_crvCOMP.address, strategy_crvCOMP.address, {"from": deployer}
    )

    # Deploy VaultSavings, Registry and add Vaults
    vaultSavingsImplFromProxy, vaultSavingsProxy, vaultSavingsImpl = deploy_proxy(
        deployer, proxy_admin, VaultSavings
    )
    print(f"VaultSavings proxy deployed at {vaultSavingsImpl.address}")
    print(f"VaultSavings implementation deployed at {vaultSavingsProxy.address}")

    registry = deployer.deploy(YTestRegistry, deployer.address)
    print(f"Registry deployed at {registry.address}")

    registry.addVault.transact(yVault_3Crv.address, {"from": deployer})
    vaultSavingsImplFromProxy.registerVault.transact(
        yVault_3Crv.address, {"from": deployer}
    )
    print("3Crv Vault registered")

    registry.addVault.transact(yVault_crvBUSD.address, {"from": deployer})
    vaultSavingsImplFromProxy.registerVault.transact(
        yVault_crvBUSD.address, {"from": deployer}
    )
    print("crvBUSD Vault registered")

    registry.addVault.transact(yVault_yUSD.address, {"from": deployer})
    vaultSavingsImplFromProxy.registerVault.transact(
        yVault_yUSD.address, {"from": deployer}
    )
    print("yUSD Vault registered")

    registry.addVault.transact(yVault_SBTC.address, {"from": deployer})
    vaultSavingsImplFromProxy.registerVault.transact(
        yVault_SBTC.address, {"from": deployer}
    )
    print("SBTC Vault registered")

    registry.addVault.transact(yVault_crvCOMP.address, {"from": deployer})
    vaultSavingsImplFromProxy.registerVault.transact(
        yVault_crvCOMP.address, {"from": deployer}
    )
    print("crvCOMP Vault registered")
