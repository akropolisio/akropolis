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
def curve(deployer, stablecoins, yTokens, token, Stub_CurveFi_SwapY, Stub_CurveFi_DepositY):
    sTokens = [stablecoins['dai'], stablecoins['usdt'], stablecoins['usdc'], stablecoins['tusd']]
    yTokens = [yTokens['yDAI'], yTokens["yUSDT"], yTokens["yUSDC"], yTokens["TUSD"]]

    # Initialization for mainnet contracts
    # token = deployer.deploy(CurveDeposit_Y, "Curve.fi yDAI/yUSDC/yUSDT/yTUSD", "yDAI+yUSDC+yUSDT+yTUSD", 18, 0)
    # swap = deployer.deploy(CurveSwap_Y, yTokens, sTokens, token, 1000, 4000000) #A = 1000, fee = 4000000 - values from Etherscan 
    # token.set_minter(swap.address, {from: deployer})
    # deposit = deployer.deploy(CurveDeposit_Y, yTokens, sTokens, swap.address, token.address)


    #token = deployer.deploy(Stub_CurveFi_LPTokenY)
    swap = deployer.deploy(Stub_CurveFi_SwapY, yTokens, sTokens, token, 4000000) #A = 1000, fee = 4000000 - values from Etherscan 
    deposit = deployer.deploy(Stub_CurveFi_DepositY, yTokens, sTokens, swap.address, token.address)
    curve = {
        token: token, 
        swap: swap, 
        deposit: deposit,
    }
    yield curve







@pytest.fixture(scope="module")
def register_vault(deployer, token, vault, strategy, controller, registry, vaultSavings, curve):
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

    #vaultSavings.registerVault.transact(vault.address, {'from': deployer})
    vaultSavings.registerVault.transact(vault.address, curve["deposit"], 4, {'from': deployer})
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

def test_deposit_only_curve_lp(register_vault, token, stablecoins, curve, vault, vaultSavings, regular_user, deployer):
    # Initial deposit
    token.mint(regular_user, DEPOSIT_VALUE)
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': regular_user})

    user_balance_before_vault = vault.balanceOf(regular_user)
    user_balance_before_token = token.balanceOf(regular_user)
    
    vaultSavings.deposit['address[],address[][],uint256[][],uint256[]'](
        [vault.address], 
        [[token.address]]
        [[DEPOSIT_VALUE]], 
        [0],
        {'from': regular_user}
    )

    user_balance_after_vault = vault.balanceOf(regular_user)
    user_balance_after_token = token.balanceOf(regular_user)

    # User sends tokens and receives vault-tokens
    assert user_balance_after_vault - user_balance_before_vault > 0 #TODO more advanced balance test
    assert user_balance_before_token - user_balance_after_token == DEPOSIT_VALUE

    # Nothing left on vaultSavings
    assert vault.balanceOf(vaultSavings.address) == 0
    assert token.balanceOf(vaultSavings.address) == 0

def test_deposit_only_one_stable(register_vault, token, stablecoins, curve, vault, vaultSavings, regular_user, deployer):
    # Initial deposit
    stablecoins['dai'].mint(regular_user, DEPOSIT_VALUE)
    stablecoins['dai'].approve(vaultSavings.address, DEPOSIT_VALUE, {'from': regular_user})

    user_balance_before_vault = vault.balanceOf(regular_user)
    user_balance_before_token = token.balanceOf(regular_user)
    user_balance_before_dai = stablecoins['dai'].balanceOf(regular_user)
    
    vaultSavings.deposit['address[],address[][],uint256[][],uint256[]'](
        [vault.address], 
        [[stablecoins['dai'].address]]
        [[DEPOSIT_VALUE]], 
        [0],
        {'from': regular_user}
    )

    user_balance_after_vault = vault.balanceOf(regular_user)
    user_balance_after_token = token.balanceOf(regular_user)
    user_balance_after_dai = stablecoins['dai'].balanceOf(regular_user)

    # User sends tokens and receives vault-tokens
    assert user_balance_after_vault - user_balance_before_vault > 0 #TODO more advanced balance test
    assert user_balance_before_dai - user_balance_after_dai == DEPOSIT_VALUE

    # Nothing left on vaultSavings
    assert vault.balanceOf(vaultSavings.address) == 0
    assert token.balanceOf(vaultSavings.address) == 0
    assert stablecoins['dai'].balanceOf(vaultSavings.address) == 0
    
def test_deposit_one_curve_lp_and_one_stable(register_vault, token, stablecoins, curve, vault, vaultSavings, regular_user, deployer):
    # Initial deposit
    token.mint(regular_user, DEPOSIT_VALUE)
    token.approve(vaultSavings.address, DEPOSIT_VALUE, {'from': regular_user})
    stablecoins['dai'].mint(regular_user, DEPOSIT_VALUE)
    stablecoins['dai'].approve(vaultSavings.address, DEPOSIT_VALUE, {'from': regular_user})

    user_balance_before_vault = vault.balanceOf(regular_user)
    user_balance_before_token = token.balanceOf(regular_user)
    user_balance_before_dai = stablecoins['dai'].balanceOf(regular_user)
    
    vaultSavings.deposit['address[],address[][],uint256[][],uint256[]'](
        [vault.address], 
        [[token.address, stablecoins['dai'].address]]
        [[DEPOSIT_VALUE/2, DEPOSIT_VALUE]], 
        [0,0],
        {'from': regular_user}
    )

    user_balance_after_vault = vault.balanceOf(regular_user)
    user_balance_after_token = token.balanceOf(regular_user)
    user_balance_after_dai = stablecoins['dai'].balanceOf(regular_user)

    # User sends tokens and receives vault-tokens
    assert user_balance_after_vault - user_balance_before_vault > 0 #TODO more advanced balance test
    assert user_balance_before_token - user_balance_after_token == DEPOSIT_VALUE/2
    assert user_balance_before_dai - user_balance_after_dai == DEPOSIT_VALUE

    # Nothing left on vaultSavings
    assert vault.balanceOf(vaultSavings.address) == 0
    assert token.balanceOf(vaultSavings.address) == 0
    assert stablecoins['dai'].balanceOf(vaultSavings.address) == 0
