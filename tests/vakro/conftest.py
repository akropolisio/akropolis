import pytest
from brownie import accounts
import sys

from utils.deploy_helpers import deploy_proxy, deploy_admin

ADEL_TO_SWAP = 100
AKRO_ON_SWAP = 10000
ADEL_AKRO_RATE = 15
EPOCH_LENGTH = 100
REWARDS_AMOUNT = 150


@pytest.fixture(scope="module")
def deployer():
    yield accounts[0]


@pytest.fixture(scope="module")
def regular_user(accounts):
    yield accounts[1]


@pytest.fixture(scope="module")
def regular_user2(accounts):
    yield accounts[2]


@pytest.fixture(scope="module")
def regular_user3(accounts):
    yield accounts[3]


@pytest.fixture(scope="module")
def regular_user4(accounts):
    yield accounts[4]


@pytest.fixture(scope="module")
def regular_user5(accounts):
    yield accounts[5]


@pytest.fixture(scope="module")
def pool(accounts):
    yield accounts[6]


@pytest.fixture(scope="module")
def proxy_admin(deployer):
    proxy_admin = deploy_admin(deployer)
    yield proxy_admin


def prepare_token(
    deployer, regular_user, regular_user2, regular_user3, TestERC20, name, symbol
):
    token = deployer.deploy(TestERC20, name, symbol, 18)
    token.mint(1500000000, {"from": deployer})
    assert token.balanceOf(deployer) == 1500000000
    token.transfer(regular_user, 1500000000 // 4, {"from": deployer})
    token.transfer(regular_user2, 1500000000 // 4, {"from": deployer})
    token.transfer(regular_user3, 1500000000 // 4, {"from": deployer})

    return token


@pytest.fixture(scope="module")
def akro(deployer, regular_user, regular_user2, regular_user3, TestERC20):
    akro = prepare_token(
        deployer, regular_user, regular_user2, regular_user3, TestERC20, "AKRO", "AKRO"
    )
    yield akro


@pytest.fixture(scope="module")
def adel(deployer, regular_user, regular_user2, regular_user3, proxy_admin, TestADEL):
    adelImplFromProxy, adelProxy, adelImpl = deploy_proxy(
        deployer, proxy_admin, TestADEL
    )

    assert adelProxy.admin.call({"from": proxy_admin.address}) == proxy_admin.address
    assert (
        adelProxy.implementation.call({"from": proxy_admin.address}) == adelImpl.address
    )

    adelImplFromProxy.mint(1500000000, {"from": deployer})
    assert adelImplFromProxy.balanceOf(deployer) == 1500000000
    adelImplFromProxy.transfer(regular_user, 1500000000 // 4, {"from": deployer})
    adelImplFromProxy.transfer(regular_user2, 1500000000 // 4, {"from": deployer})
    adelImplFromProxy.transfer(regular_user3, 1500000000 // 4, {"from": deployer})

    yield adelImplFromProxy


@pytest.fixture(scope="module")
def vakro(deployer, proxy_admin, akro, VestedAkro):
    vakroImplFromProxy, vakroProxy, vakroImpl = deploy_proxy(
        deployer, proxy_admin, VestedAkro, akro.address, EPOCH_LENGTH
    )

    assert vakroProxy.admin.call({"from": proxy_admin.address}) == proxy_admin.address
    assert (
        vakroProxy.implementation.call({"from": proxy_admin.address})
        == vakroImpl.address
    )

    yield vakroImplFromProxy


@pytest.fixture(scope="module")
def stakingpool(deployer, proxy_admin, pool, adel, TestStakingPool):
    stakingpoolImplFromProxy, stakingpoolProxy, stakingpoolImpl = deploy_proxy(
        deployer, proxy_admin, TestStakingPool, pool, adel.address, EPOCH_LENGTH
    )

    assert (
        stakingpoolProxy.admin.call({"from": proxy_admin.address})
        == proxy_admin.address
    )
    assert (
        stakingpoolProxy.implementation.call({"from": proxy_admin.address})
        == stakingpoolImpl.address
    )

    assert stakingpoolImplFromProxy.owner() == deployer.address

    yield stakingpoolImplFromProxy


@pytest.fixture(scope="module")
def vakroSwap(deployer, proxy_admin, adel, akro, vakro, AdelVAkroSwap):
    vakroSwapImplFromProxy, vakroSwapProxy, vakroSwapImpl = deploy_proxy(
        deployer, proxy_admin, AdelVAkroSwap, akro.address, adel.address, vakro.address
    )

    assert (
        vakroSwapProxy.admin.call({"from": proxy_admin.address}) == proxy_admin.address
    )
    assert (
        vakroSwapProxy.implementation.call({"from": proxy_admin.address})
        == vakroSwapImpl.address
    )

    yield vakroSwapImplFromProxy


@pytest.fixture(scope="module")
def testVakroSwap(deployer, proxy_admin, adel, akro, vakro, TestAdelVAkroSwap):
    vakroSwapImplFromProxy, vakroSwapProxy, vakroSwapImpl = deploy_proxy(
        deployer,
        proxy_admin,
        TestAdelVAkroSwap,
        akro.address,
        adel.address,
        vakro.address,
    )

    assert (
        vakroSwapProxy.admin.call({"from": proxy_admin.address}) == proxy_admin.address
    )
    assert (
        vakroSwapProxy.implementation.call({"from": proxy_admin.address})
        == vakroSwapImpl.address
    )

    yield vakroSwapImplFromProxy


@pytest.fixture(scope="module")
def testVakroVestingSwap(
    deployer, proxy_admin, adel, akro, vakro, TestAdelVAkroVestingSwap
):
    (
        vakroVestingSwapImplFromProxy,
        vakroVestingSwapProxy,
        vakroVestingSwapImpl,
    ) = deploy_proxy(
        deployer,
        proxy_admin,
        TestAdelVAkroVestingSwap,
        akro.address,
        adel.address,
        vakro.address,
    )

    assert (
        vakroVestingSwapProxy.admin.call({"from": proxy_admin.address})
        == proxy_admin.address
    )
    assert (
        vakroVestingSwapProxy.implementation.call({"from": proxy_admin.address})
        == vakroVestingSwapImpl.address
    )

    yield vakroVestingSwapImplFromProxy


@pytest.fixture(scope="module")
def exploitCompVAkroSwap(deployer, proxy_admin, adel, akro, vakro, ExploitCompVAkroSwap):
    vakroSwapImplFromProxy, vakroSwapProxy, vakroSwapImpl = deploy_proxy(deployer, proxy_admin, ExploitCompVAkroSwap,
                                                                         vakro.address)

    assert vakroSwapProxy.admin.call({"from":proxy_admin.address}) == proxy_admin.address
    assert vakroSwapProxy.implementation.call({"from":proxy_admin.address}) == vakroSwapImpl.address


    yield vakroSwapImplFromProxy


@pytest.fixture(scope="module")
def testExploitCompVAkroSwap(deployer, proxy_admin, adel, akro, vakro, TestExploitCompVAkroSwap):
    vakroSwapImplFromProxy, vakroSwapProxy, vakroSwapImpl = deploy_proxy(deployer, proxy_admin, TestExploitCompVAkroSwap,
                                                                         vakro.address)

    assert vakroSwapProxy.admin.call({"from":proxy_admin.address}) == proxy_admin.address
    assert vakroSwapProxy.implementation.call({"from":proxy_admin.address}) == vakroSwapImpl.address

    yield vakroSwapImplFromProxy

@pytest.fixture(scope="module")
def rewardmodule(deployer, pool, proxy_admin, TestRewardVestingModule):
    rewardmoduleImplFromProxy, rewardmoduleProxy, rewardmoduleImpl = deploy_proxy(
        deployer, proxy_admin, TestRewardVestingModule, pool
    )

    assert (
        rewardmoduleProxy.admin.call({"from": proxy_admin.address})
        == proxy_admin.address
    )
    assert (
        rewardmoduleProxy.implementation.call({"from": proxy_admin.address})
        == rewardmoduleImpl.address
    )

    assert rewardmoduleImplFromProxy.owner() == deployer.address

    yield rewardmoduleImplFromProxy


@pytest.fixture(scope="module")
def setup_rewards(chain, deployer, adel, stakingpool, rewardmodule):
    rewardmodule.registerRewardToken(
        stakingpool.address, adel.address, 0, {"from": deployer}
    )
    rewardmodule.setDefaultEpochLength(EPOCH_LENGTH, {"from": deployer})
    adel.approve(rewardmodule.address, REWARDS_AMOUNT, {"from": deployer})
    rewardmodule.createEpoch(
        stakingpool.address,
        adel.address,
        chain.time() + EPOCH_LENGTH,
        REWARDS_AMOUNT,
        {"from": deployer},
    )

    stakingpool.registerRewardToken(adel.address, {"from": deployer})
    stakingpool.setRewardVesting(rewardmodule.address, {"from": deployer})
