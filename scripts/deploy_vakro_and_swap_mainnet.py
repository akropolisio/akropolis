import os
from dotenv import load_dotenv, find_dotenv
from brownie import *

# VestedAkro, AdelVAkroSwap, accounts, network, web3

from utils.deploy_helpers import (
    deploy_proxy,
    deploy_admin,
    get_proxy_admin,
    upgrade_proxy,
    deploy_proxy_over_impl,
)


def main():
    # load_dotenv(dotenv_path=Path('..')/".env", override=True)

    load_dotenv(find_dotenv())

    print(f"You are using the '{network.show_active()}' network")
    deployer = accounts.add(os.getenv("DEPLOYER_PRIVATE_KEY"))
    proxy_admin = os.getenv("MAINNET_PROXY_ADMIN")

    print(f"You are using: 'deployer' [{deployer.address}]")
    print(f"Proxy Admin at {proxy_admin}")

    mainet_vakro = os.getenv("MAINNET_VAKRO")
    mainnet_swap = os.getenv("MAINNET_SWAP")
    mainnet_akro_address = os.getenv("MAINNET_AKRO_PROXY")
    mainnet_adel_address = os.getenv("MAINNET_ADEL_PROXY")
    mainnet_adel_staking_address = os.getenv("MAINNET_ADEL_STAKING_PROXY")
    mainnet_akro_staking_address = os.getenv("MAINNET_AKRO_STAKING_PROXY")
    mainnet_vakro_minter = os.getenv("MAINNET_VAKRO_MINTER")

    print(mainet_vakro)
    print(mainnet_swap)
    print(mainnet_akro_address)
    print(mainnet_adel_address)
    print(mainnet_adel_staking_address)
    print(mainnet_akro_staking_address)
    print(mainnet_vakro_minter)

    mainnet_vakro_vesting_period = 60 * 60 * 24 * 365 * 2  # 2 years - 24 month
    mainnet_vakro_start_date = 1622505600  # 1 June 2021, 00:00:00 UTC+0
    mainnet_vakro_cliff = 0  # no cliff

    mainnet_swap_num = 15
    mainnet_swap_denom = 1

    if network.show_active() == "mainnet" or network.show_active() == "development":
        # Deploy vAkro
        vakroImplFromProxy, vakroProxy = deploy_proxy_over_impl(
            deployer,
            proxy_admin,
            mainet_vakro,
            VestedAkro,
            mainnet_akro_address,
            mainnet_vakro_vesting_period,
        )

        print(f"vAkro proxy deployed at {vakroProxy.address}")
        print(f"vAkro implementation deployed at {mainet_vakro}")

        # Deploy Swap contract
        vakroSwapImplFromProxy, vakroSwapProxy = deploy_proxy_over_impl(
            deployer,
            proxy_admin,
            mainnet_swap,
            AdelVAkroSwap,
            mainnet_akro_address,
            mainnet_adel_address,
            vakroImplFromProxy.address,
        )

        print(f"Swap proxy deployed at {vakroSwapProxy.address}")
        print(f"Swap implementation deployed at {mainnet_swap}")

        print("==== Setup contracts ====")
        vakroImplFromProxy.setVestingCliff(mainnet_vakro_cliff, {"from": deployer})
        vakroImplFromProxy.setVestingStart(mainnet_vakro_start_date, {"from": deployer})

        print(f"Settings for vAkro (in seconds):")
        print(f"Vesting period: {mainnet_vakro_vesting_period}")
        print(f"Vesting start: {mainnet_vakro_start_date}")
        print(f"Vesting cliff: {mainnet_vakro_cliff}")

        vakroSwapImplFromProxy.setSwapRate(
            mainnet_swap_num, mainnet_swap_denom, {"from": deployer}
        )
        vakroSwapImplFromProxy.setStakingPool(
            mainnet_adel_staking_address, {"from": deployer}
        )
        vakroSwapImplFromProxy.setRewardStakingPool(
            mainnet_akro_staking_address,
            mainnet_adel_staking_address,
            {"from": deployer},
        )

        vakroImplFromProxy.addMinter(vakroSwapImplFromProxy.address, {"from": deployer})
        vakroImplFromProxy.addSender(vakroSwapImplFromProxy.address, {"from": deployer})

        print(f"Settings for Swap:")
        print(f"swap rate: {mainnet_swap_num / mainnet_swap_denom}")

        vakroImplFromProxy.addMinter(mainnet_vakro_minter, {"from": deployer})
        vakroImplFromProxy.addSender(mainnet_vakro_minter, {"from": deployer})

        print(f"{mainnet_vakro_minter} added as minter and sender for vAkro")
