import pytest
import brownie

@pytest.fixture(scope="module")
def stablecoins(deployer, TestERC20):
    stablecoins = {
        dai: deployer.deploy(TestERC20, "Dai Stablecoin", "DAI", 18),
        usdt: deployer.deploy(TestERC20, "Tether USD", "USDT", 6),
        usdc: deployer.deploy(TestERC20, "USD Coin", "USDC", 6),
        tusd: deployer.deploy(TestERC20, "TrueUSD", "TUSD", 18),
    }
    yield stablecoins

@pytest.fixture(scope="module")
def yTokens(deployer, stablecoins, YTokenStub):
    yTokens = {
        yDAI: deployer.deploy(YTokenStub, stablecoins['dai'].address, "DAI", 18),
        yUSDT: deployer.deploy(YTokenStub, stablecoins['usdt'].address, "USDT", 6),
        yUSDC: deployer.deploy(YTokenStub, stablecoins['usdc'].address, "USDC", 6),
        yTUSD: deployer.deploy(YTokenStub, stablecoins['tusd'].address, "TUSD", 18),
    }
    yield yTokens

@pytest.fixture(scope="module")
def curve(deployer, stablecoins, yTokens, CurveToken_Y, CurveSwap_Y, CurveDeposit_Y):
    token = deployer.deploy(CurveDeposit_Y, "Curve.fi yDAI/yUSDC/yUSDT/yTUSD", "yDAI+yUSDC+yUSDT+yTUSD", 18, 0)
    baseTokens = [stablecoins['dai'], stablecoins['usdt'], stablecoins['usdc'], stablecoins['tusd']]
    underlyingTokens = [yTokens['yDAI'], yTokens["yUSDT"], yTokens["yUSDC"], yTokens["TUSD"]]
    swap = deployer.deploy(CurveSwap_Y, underlyingTokens, baseTokens, token, 1000, 4000000) #A = 1000, fee = 4000000 - values from Etherscan 
    token.set_minter(swap.address, {from: deployer})
    deposit = deployer.deploy(CurveDeposit_Y, underlyingTokens, baseTokens, swap.address, token.address)
    curve = [token, swap, deposit]
    yield curve







@pytest.fixture(scope="module")
def register_vault(deployer, token, vault, strategy, controller, registry, vaultSavings):
    controller.setVault(token.address, vault.address, {'from': deployer})
    controller.approveStrategy(token.address, strategy.address, {'from': deployer})
    controller.setStrategy(token.address, strategy.address, {'from': deployer})

    assert registry.getVaultsLength() == 0
    registry.addVault.transact(vault.address, {'from': deployer})
    assert registry.getVaultsLength() == 1
    assert registry.getVault(0) == vault.address
    vaults_arr = registry.getVaults()
    assert len(vaults_arr) == 1
    assert vaults_arr[0] == vault.address

    vaultSavings.registerVault.transact(vault.address, {'from': deployer})
    assert vaultSavings.isVaultRegistered(vault.address) == True
    assert vaultSavings.isVaultActive(vault.address) == True
    assert vaultSavings.isBaseTokenForVault(vault.address, token.address) == True
    supported_vaults = vaultSavings.supportedVaults()
    assert len(supported_vaults) == 1
    assert supported_vaults[0] == vault.address
    active_vaults = vaultSavings.activeVaults()
    assert len(active_vaults) == 1
    assert active_vaults[0] == vault.address

DEPOSIT_VALUE = 2000000

def test_deposit(register_vault, token, vault, vaultSavings, regular_user, deployer):
    # Initial deposit
    user_balance_before = token.balanceOf(regular_user)
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': regular_user})
    vaultSavings.deposit['address,uint'](vault.address, DEPOSIT_VALUE, {'from': regular_user})

    user_balance_after = token.balanceOf(regular_user)

    # User sends tokens and receives LP-tokens
    assert user_balance_before - user_balance_after == DEPOSIT_VALUE
    assert token.balanceOf(vault.address) == DEPOSIT_VALUE

    # First deposit - exect amount
    assert vault.balanceOf(regular_user) == DEPOSIT_VALUE
    assert vault.totalSupply() == DEPOSIT_VALUE

    # Nothing left on vaultSavings
    assert vault.balanceOf(vaultSavings.address) == 0
    assert token.balanceOf(vaultSavings.address) == 0

    # For test vault - custom logic
    assert vault.available() == DEPOSIT_VALUE * vault.min() // vault.max()
    assert vault.balance() == DEPOSIT_VALUE
