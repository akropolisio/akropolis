import pytest
from brownie import accounts, compile_source, TestVaultV2
import sys
from constantsV2 import *
from utils.deploy_helpers import deploy_proxy, deploy_admin
from pathlib import Path
from functools import lru_cache
from eth_account import Account
from eth_account.messages import encode_structured_data

VAULT_SOURCE_CODE = (Path(__file__).parents[2] / "contracts/test/yearnV2/TestVaultV2.vy").read_text()
PACKAGE_VERSION="0.3.4"

@pytest.fixture
def patch_vault_version():
    # NOTE: Cache this result so as not to trigger a recompile for every version change
    @lru_cache
    def patch_vault_version(version):
        if version is None:
            return TestVaultV2
        else:
            source = VAULT_SOURCE_CODE.replace(PACKAGE_VERSION, version)
            return compile_source(source).Vyper

    return patch_vault_version

@pytest.fixture(scope="function")
def deployer():
    yield accounts[0]

@pytest.fixture(scope="function")
def gov():
    yield accounts[7]

@pytest.fixture(scope="function")
def affiliate():
    yield accounts[0] 

@pytest.fixture(scope="function")
def rewards(accounts):
    yield accounts[1]

@pytest.fixture(scope="function")
def strategist():
    yield accounts[2]

@pytest.fixture(scope="function")
def regular_user(accounts):
    yield accounts[3]

@pytest.fixture(scope="function")
def regular_user2(accounts):
    yield accounts[4]

@pytest.fixture(scope="function")
def investment(accounts):
    yield accounts[5]

@pytest.fixture(scope="function")
def investment2(accounts):
    yield accounts[6]

@pytest.fixture
def rando(accounts):
    yield accounts[9]


def prepare_token(deployer, gov, TestERC20):
    token = deployer.deploy(TestERC20, "Test Token", "TST", 18)
    token.mint(TOTAL_TOKENS, {"from": deployer})
    assert token.balanceOf(deployer) == TOTAL_TOKENS
    token.transfer(gov, TOTAL_TOKENS, {"from": deployer})

    return token

@pytest.fixture(scope="function")
def token(deployer, gov, TestERC20):
    token = prepare_token(deployer, gov, TestERC20)
    yield token

def Token(token):
    yield token

@pytest.fixture(scope="function")
def token2(deployer, regular_user, regular_user2, TestERC20):
    token = prepare_token(deployer, regular_user, regular_user2, TestERC20)
    yield token

@pytest.fixture(scope="function")
def create_vault(deployer, gov, rewards, token, patch_vault_version, TestERC20):
    def create_vault(token=None, version=None, governance=gov):
        if token is None:
            token = prepare_token(deployer, gov, TestERC20)
        
        vault = patch_vault_version(version).deploy({"from": deployer})
        vault.initialize(token, gov, rewards, "", "", deployer)
        vault.setDepositLimit(2 ** 256 - 1, {"from": gov})

        return vault
    return create_vault


@pytest.fixture(scope="function")
def vault(token, create_vault, gov):
    vault = create_vault(token=token, governance=gov)
    yield vault

@pytest.fixture(scope="function")
def vault2(token, create_vault, gov):
    vault = create_vault(version="2.0.0", governance=gov)
    yield vault


def prepare_strategy(strategist, deployer, vault, token, investment, StubStrategyV2):
    strategy = strategist.deploy(StubStrategyV2, vault, investment, STUB_YIELD)
    token.approve(strategy, 10**18, {"from":investment})
    strategy.setKeeper(strategist, {"from": strategist})

    return strategy

@pytest.fixture(scope="function")
def strategy(strategist, deployer, vault, token, investment, StubStrategyV2):
    strategy = prepare_strategy(strategist, deployer, vault, token, investment, StubStrategyV2)

    yield strategy


@pytest.fixture(scope="function")
def strategy_vault2(strategist, deployer, vault2, token2, investment2, StubStrategyV2):
    strategy = prepare_strategy(strategist, deployer, vault2, token2, investment2, StubStrategyV2)

    yield strategy

@pytest.fixture(scope="function")
def strategy2(strategist, deployer, vault, token, investment2, StubStrategyV2):
    strategy = prepare_strategy(strategist, deployer, vault, token, investment2, StubStrategyV2)

    yield strategy

@pytest.fixture(scope="function")
def registry(deployer, gov, TestRegistryV2):
    registry = deployer.deploy(TestRegistryV2)
    registry.setGovernance(gov,  {"from": deployer})
    registry.acceptGovernance({"from": gov})
    assert registry.governance() == gov
    yield registry

@pytest.fixture(scope="function")
def proxy_admin(deployer):
    proxy_admin = deploy_admin(deployer)
    yield proxy_admin

@pytest.fixture(scope="function")
def affiliate_token(token, affiliate, registry, AffiliateToken):
    # Affliate Wrapper
    yield affiliate.deploy(
        AffiliateToken,
        token,
        registry,
        f"Affiliate {token.symbol()}",
        f"af{token.symbol()}",
    )


@pytest.fixture(scope="function")
def register_vault_in_system(deployer, gov, token, vault, strategy, registry):
    assert registry.vaults(token.address, 0) == NULL_ADDRESS
    registry.newRelease(vault.address, {'from': deployer})
    assert registry.vaults(token.address, 0) == vault.address
    
    vault.addStrategy(strategy, STRAT_DEBT_RATIO, STRAT_OPERATION_LIMIT, STRAT_OPERATION_FEE, {"from": gov})

@pytest.fixture(scope="function")
def vault_add_second_strategy(deployer, gov, token, vault, strategy2, registry):    
    vault.addStrategy(strategy2, STRAT_DEBT_RATIO, STRAT_OPERATION_LIMIT, STRAT_OPERATION_FEE, {"from": gov})

@pytest.fixture(scope="function")
def register_vault2_in_system(deployer, gov, token2, vault2, strategy_vault2, registry):
    registry.endorseVault(vault2.address, {'from': deployer})
    
    vault2.addStrategy(strategy_vault2, STRAT_DEBT_RATIO, STRAT_OPERATION_LIMIT, STRAT_OPERATION_FEE, {"from": gov})

@pytest.fixture
def sign_token_permit():
    def sign_token_permit(
        token: Token,
        owner: Account,  # NOTE: Must be a eth_key account, not Brownie
        spender: str,
        allowance: int = 2 ** 256 - 1,  # Allowance to set with `permit`
        deadline: int = 0,  # 0 means no time limit
        override_nonce: int = None,
    ):
        chain_id = 1  # ganache bug https://github.com/trufflesuite/ganache/issues/1643
        if override_nonce:
            nonce = override_nonce
        else:
            nonce = token.nonces(owner.address)
        data = {
            "types": {
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                    {"name": "verifyingContract", "type": "address"},
                ],
                "Permit": [
                    {"name": "owner", "type": "address"},
                    {"name": "spender", "type": "address"},
                    {"name": "value", "type": "uint256"},
                    {"name": "nonce", "type": "uint256"},
                    {"name": "deadline", "type": "uint256"},
                ],
            },
            "domain": {
                "name": token.name(),
                "version": "1",
                "chainId": chain_id,
                "verifyingContract": str(token),
            },
            "primaryType": "Permit",
            "message": {
                "owner": owner.address,
                "spender": spender,
                "value": allowance,
                "nonce": nonce,
                "deadline": deadline,
            },
        }
        permit = encode_structured_data(data)
        return owner.sign_message(permit)

    return sign_token_permit




