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

    rinkeby_akro_address = os.getenv("RINKEBY_AKRO")
    rinkeby_adel_address = os.getenv("RINKEBY_ADEL")
    rinkeby_adel_staking_address = os.getenv("RINKEBY_ADEL_STAKING")
    rinkeby_akro_staking_address = os.getenv("RINKEBY_AKRO_STAKING")
    rinkeby_vakro_minter = os.getenv("RINKEBY_VAKRO_MINTER")
    rinkeby_vakro_vesting_period = 60 * 60 * 24 * 30  # 1 month
    rinkeby_vakro_start_date = 1613606400  # 18 Feb 2021, 00:00:00 UTC+0
    rinkeby_vakro_cliff = 60 * 60 * 24  # 1 day

    rinkeby_swap_num = 15
    rinkeby_swap_denom = 1

    if network.show_active() == "rinkeby" or network.show_active() == "development":
        # Deploy vAkro
        vakroImplFromProxy, vakroProxy, vakroImpl = deploy_proxy(
            deployer,
            proxy_admin,
            VestedAkro,
            rinkeby_akro_address,
            rinkeby_vakro_vesting_period,
        )

        print(f"vAkro proxy deployed at {vakroProxy.address}")
        print(f"vAkro implementation deployed at {vakroImpl.address}")

        vakroImplFromProxy.setVestingCliff(rinkeby_vakro_cliff, {"from": deployer})
        vakroImplFromProxy.setVestingStart(rinkeby_vakro_start_date, {"from": deployer})

        print(f"Settings for vAkro (in seconds):")
        print(f"Vesting period: {rinkeby_vakro_vesting_period}")
        print(f"Vesting start: {rinkeby_vakro_start_date}")
        print(f"Vesting cliff: {rinkeby_vakro_cliff}")

        vakroSwapImpl = os.getenv("RINKEBY_VAKRO_SWAP")
        # Deploy Swap contract
        vakroSwapImplFromProxy, vakroSwapProxy = deploy_proxy_over_impl(
            deployer,
            proxy_admin,
            vakroSwapImpl,
            AdelVAkroSwap,
            rinkeby_akro_address,
            rinkeby_adel_address,
            vakroImplFromProxy.address,
        )

        print(f"Swap proxy deployed at {vakroSwapProxy.address}")
        print(f"Swap implementation deployed at {vakroSwapImpl}")

        vakroSwapImplFromProxy.setSwapRate(
            rinkeby_swap_num, rinkeby_swap_denom, {"from": deployer}
        )
        vakroSwapImplFromProxy.setStakingPool(
            rinkeby_adel_staking_address, {"from": deployer}
        )
        vakroSwapImplFromProxy.setRewardStakingPool(
            rinkeby_akro_staking_address,
            rinkeby_adel_staking_address,
            {"from": deployer},
        )

        vakroImplFromProxy.addMinter(vakroSwapImplFromProxy.address, {"from": deployer})
        vakroImplFromProxy.addSender(vakroSwapImplFromProxy.address, {"from": deployer})

        print(f"Settings for Swap:")
        print(f"swap rate: {rinkeby_swap_num / rinkeby_swap_denom}")

        vakroImplFromProxy.addMinter(rinkeby_vakro_minter, {"from": deployer})
        vakroImplFromProxy.addSender(rinkeby_vakro_minter, {"from": deployer})

        print(f"{rinkeby_vakro_minter} added as minter and sender for vAkro")

        # Deploy Vesting Swap contract
        vakroVestingSwapImpl = os.getenv("RINKEBY_VAKRO_VESTING_SWAP")
        vakroVestingSwapImplFromProxy, vakroVestingSwapProxy = deploy_proxy_over_impl(
            deployer,
            proxy_admin,
            vakroVestingSwapImpl,
            AdelVAkroVestingSwap,
            rinkeby_akro_address,
            rinkeby_adel_address,
            vakroImplFromProxy.address,
        )

        print(f"Swap from vesting proxy deployed at {vakroVestingSwapProxy.address}")
        print(f"Swap from vesting implementation deployed at {vakroVestingSwapImpl}")

        vakroVestingSwapImplFromProxy.setSwapRate(
            rinkeby_swap_num, rinkeby_swap_denom, {"from": deployer}
        )

        vakroImplFromProxy.addMinter(
            vakroVestingSwapImplFromProxy.address, {"from": deployer}
        )
        vakroImplFromProxy.addSender(
            vakroVestingSwapImplFromProxy.address, {"from": deployer}
        )

        print(f"Settings for Swap:")
        print(f"swap rate: {rinkeby_swap_num / rinkeby_swap_denom}")
