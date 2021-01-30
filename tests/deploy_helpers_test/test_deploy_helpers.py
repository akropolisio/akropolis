import pytest
from brownie import accounts, UpgradeTestOld, UpgradeTestNew

from utils.deploy_helpers import deploy_proxy, deploy_admin, upgrade_proxy

@pytest.fixture(scope="module")
def deployer():
    yield accounts[0]

@pytest.fixture(scope="module")
def admin_address():
    yield accounts[1]

@pytest.fixture(scope="module")
def admin_contract(deployer):
    admin_contract = deploy_admin(deployer)
    yield admin_contract


def test_helpers_with_admin_contract(deployer, admin_contract, UpgradeTestOld, UpgradeTestNew):
    init_arg = 10
    testImplFromProxy, testProxy, testImpl = deploy_proxy(deployer, admin_contract, UpgradeTestOld, init_arg)

    assert testProxy.admin.call({"from": admin_contract}) == admin_contract.address
    assert testProxy.implementation.call({"from":admin_contract}) == testImpl.address

    assert testImplFromProxy.oldStorage() == init_arg
    assert testImplFromProxy.upgrateTest() == 1

    newTestImplFromProxy, newTestImpl = upgrade_proxy(deployer, admin_contract, testProxy, UpgradeTestNew)

    assert testProxy.implementation.call({"from": admin_contract}) == newTestImpl.address

    assert newTestImplFromProxy.oldStorage() == init_arg
    assert newTestImplFromProxy.upgrateTest() == 2


def test_helpers_with_admin_address(deployer, admin_address, UpgradeTestOld, UpgradeTestNew):
    init_arg = 20
    testImplFromProxy, testProxy, testImpl = deploy_proxy(deployer, admin_address, UpgradeTestOld, init_arg)

    assert testProxy.admin.call({"from": admin_address}) == admin_address.address
    assert testProxy.implementation.call({"from": admin_address}) == testImpl.address

    assert testImplFromProxy.oldStorage() == init_arg
    assert testImplFromProxy.upgrateTest() == 1

    newTestImplFromProxy, newTestImpl = upgrade_proxy(deployer, admin_address, testProxy, UpgradeTestNew)

    assert testProxy.implementation.call({"from": admin_address}) == newTestImpl.address

    assert newTestImplFromProxy.oldStorage() == init_arg
    assert newTestImplFromProxy.upgrateTest() == 2