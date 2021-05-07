import pytest
import brownie

from constants import *
from utils.utils import amount_in_small_dimension


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_successful_buy(indices_savings_swap, tokens, uniswap_router, regular_user, deployer):
    buy_amount = amount_in_small_dimension(10, tokens[TOKEN_TOKEN1])
    buy_amount_out_min = uniswap_router.getAmountsOut(
        buy_amount,
        [tokens[TOKEN_TOKEN1].address, tokens[TOKEN_INDEX1].address]
     )[-1]
    assert buy_amount * 2 == buy_amount_out_min

    tokens[TOKEN_TOKEN1].transfer(regular_user, buy_amount, {'from': deployer})

    token_balance_before = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    index_balance_before = tokens[TOKEN_INDEX1].balanceOf(regular_user)

    tokens[TOKEN_TOKEN1].approve(indices_savings_swap.address, buy_amount, {'from': regular_user})

    path = [tokens[TOKEN_TOKEN1].address, tokens[TOKEN_INDEX1].address]
    indices_savings_swap.buy['address,address,uint,uint,address[]'](
        tokens[TOKEN_INDEX1].address,
        tokens[TOKEN_TOKEN1].address,
        buy_amount,
        buy_amount_out_min,
        path,
        {'from': regular_user}
        )

    token_balance_after = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    index_balance_after = tokens[TOKEN_INDEX1].balanceOf(regular_user)

    assert buy_amount > 0
    assert buy_amount_out_min > 0
    assert token_balance_before - token_balance_after == buy_amount
    assert index_balance_after - index_balance_before >= buy_amount_out_min


def test_successful_sell(indices_savings_swap, tokens, uniswap_router, regular_user, deployer):
    sell_amount = amount_in_small_dimension(0.005, tokens[TOKEN_INDEX1])
    sell_amount_out_min = uniswap_router.getAmountsOut(
        sell_amount,
        [tokens[TOKEN_INDEX1].address, tokens[TOKEN_TOKEN1].address]
     )[-1]
    assert sell_amount / 2 == sell_amount_out_min

    tokens[TOKEN_INDEX1].transfer(regular_user, sell_amount, {'from': deployer})

    token_balance_before = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    index_balance_before = tokens[TOKEN_INDEX1].balanceOf(regular_user)

    tokens[TOKEN_INDEX1].approve(indices_savings_swap.address, sell_amount, {'from': regular_user})

    path = [tokens[TOKEN_INDEX1].address, tokens[TOKEN_TOKEN1].address]
    indices_savings_swap.sell['address,address,uint,uint,address[]'](
        tokens[TOKEN_INDEX1].address,
        tokens[TOKEN_TOKEN1].address,
        sell_amount,
        sell_amount_out_min,
        path,
        {'from': regular_user}
        )

    token_balance_after = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    index_balance_after = tokens[TOKEN_INDEX1].balanceOf(regular_user)

    assert sell_amount > 0
    assert sell_amount_out_min > 0
    assert index_balance_before - index_balance_after == sell_amount
    assert token_balance_after - token_balance_before >= sell_amount_out_min


def test_successful_buy_eth(indices_savings_swap, tokens, uniswap_router, regular_user, deployer):
    buy_amount = int(1 * (10 ** WETH_DECIMALS) / 50000)
    buy_amount_out_min = uniswap_router.getAmountsOut(
        buy_amount,
        [tokens[TOKEN_WETH].address, tokens[TOKEN_INDEX1].address]
     )[-1]
    assert buy_amount * 1000000 == buy_amount_out_min

    eth_balance_before = regular_user.balance()
    index_balance_before = tokens[TOKEN_INDEX1].balanceOf(regular_user)
    assert buy_amount < eth_balance_before

    path = [tokens[TOKEN_WETH].address, tokens[TOKEN_INDEX1].address]
    indices_savings_swap.buy['address,address,uint,uint,address[]'](
        tokens[TOKEN_INDEX1].address,
        ETH_ADDRESS,
        buy_amount,
        buy_amount_out_min,
        path,
        {'from': regular_user, "value": str(buy_amount) + " wei" }
        )

    eth_balance_after = regular_user.balance()
    index_balance_after = tokens[TOKEN_INDEX1].balanceOf(regular_user)

    assert buy_amount > 0
    assert buy_amount_out_min > 0
    assert eth_balance_before - eth_balance_after >= buy_amount # fee for tx can make error
    assert index_balance_after - index_balance_before >= buy_amount_out_min


def test_successful_sell_eth(indices_savings_swap, tokens, uniswap_router, regular_user, deployer):
    sell_amount = amount_in_small_dimension(0.1, tokens[TOKEN_INDEX1])
    sell_amount_out_min = uniswap_router.getAmountsOut(
        sell_amount,
        [tokens[TOKEN_INDEX1].address, tokens[TOKEN_WETH].address]
     )[-1]
    assert sell_amount / 1000000 == sell_amount_out_min
    assert tokens[TOKEN_WETH].balance() >= sell_amount_out_min

    tokens[TOKEN_INDEX1].transfer(regular_user, sell_amount, {'from': deployer})

    index_balance_before = tokens[TOKEN_INDEX1].balanceOf(regular_user)
    eth_balance_before = regular_user.balance()

    tokens[TOKEN_INDEX1].approve(indices_savings_swap.address, sell_amount, {'from': regular_user})

    path = [tokens[TOKEN_INDEX1].address, tokens[TOKEN_WETH].address]
    indices_savings_swap.sell['address,address,uint,uint,address[]'](
        tokens[TOKEN_INDEX1].address,
        ETH_ADDRESS,
        sell_amount,
        sell_amount_out_min,
        path,
        {'from': regular_user}
        )

    index_balance_after = tokens[TOKEN_INDEX1].balanceOf(regular_user)
    eth_balance_after = regular_user.balance()

    assert sell_amount > 0
    assert sell_amount_out_min > 0
    assert index_balance_before - index_balance_after == sell_amount
    assert eth_balance_after - eth_balance_before >= sell_amount_out_min # fee for tx can make error


def test_successful_multiple_purchases(indices_savings_swap, tokens, uniswap_router, uniswap_router2, regular_user, deployer):
    buy_amounts = [
        amount_in_small_dimension(10, tokens[TOKEN_TOKEN1]),
        int(1 * (10 ** WETH_DECIMALS) / 50000)
    ]
    buy_amounts_out_min = [
         uniswap_router.getAmountsOut(
                buy_amounts[0],
                [tokens[TOKEN_TOKEN1].address, tokens[TOKEN_INDEX1].address]
             )[-1],
         uniswap_router2.getAmountsOut(
                 buy_amounts[1],
                 [tokens[TOKEN_WETH].address, tokens[TOKEN_INDEX2].address]
              )[-1]
    ]
    assert buy_amounts[0] * 2 == buy_amounts_out_min[0]
    assert buy_amounts[1] * 1000000 == buy_amounts_out_min[1]

    tokens[TOKEN_TOKEN1].transfer(regular_user, buy_amounts[0], {'from': deployer})

    token_balance_before = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    eth_balance_before = regular_user.balance()
    index1_balance_before = tokens[TOKEN_INDEX1].balanceOf(regular_user)
    index2_balance_before = tokens[TOKEN_INDEX2].balanceOf(regular_user)

    assert buy_amounts[0] <= token_balance_before
    assert buy_amounts[1] <= eth_balance_before

    tokens[TOKEN_TOKEN1].approve(indices_savings_swap.address, buy_amounts[0], {'from': regular_user})

    paths = [
        [tokens[TOKEN_TOKEN1].address, tokens[TOKEN_INDEX1].address],
        [tokens[TOKEN_WETH].address, tokens[TOKEN_INDEX2].address]
    ]
    indices_savings_swap.buy['address[],address[],uint[],uint[],address[][]'](
        [tokens[TOKEN_INDEX1].address, tokens[TOKEN_INDEX2].address],
        [tokens[TOKEN_TOKEN1].address, ETH_ADDRESS],
        buy_amounts,
        buy_amounts_out_min,
        paths,
        {'from': regular_user, "value": str(buy_amounts[1]) + " wei" }
        )

    token_balance_after = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    eth_balance_after = regular_user.balance()
    index1_balance_after = tokens[TOKEN_INDEX1].balanceOf(regular_user)
    index2_balance_after = tokens[TOKEN_INDEX2].balanceOf(regular_user)

    assert token_balance_before - token_balance_after == buy_amounts[0]
    assert eth_balance_before - eth_balance_after >= buy_amounts[1] # fee for tx can make error
    assert index1_balance_after - index1_balance_before >= buy_amounts_out_min[0]
    assert index2_balance_after - index2_balance_before >= buy_amounts_out_min[1]


def test_successful_multiple_sales(indices_savings_swap, tokens, uniswap_router, uniswap_router2, regular_user, deployer):
    sell_amounts = [
        amount_in_small_dimension(0.005, tokens[TOKEN_INDEX1]),
        amount_in_small_dimension(0.1, tokens[TOKEN_INDEX2])
    ]
    sell_amounts_out_min = [
        uniswap_router.getAmountsOut(
                sell_amounts[0],
                [tokens[TOKEN_INDEX1].address, tokens[TOKEN_TOKEN1].address]
             )[-1],
        uniswap_router2.getAmountsOut(
                sell_amounts[1],
                [tokens[TOKEN_INDEX2].address, tokens[TOKEN_WETH].address]
             )[-1]
    ]
    assert sell_amounts[0] / 2 == sell_amounts_out_min[0]
    assert sell_amounts[1] / 1000000 == sell_amounts_out_min[1]

    tokens[TOKEN_INDEX1].transfer(regular_user, sell_amounts[0], {'from': deployer})
    tokens[TOKEN_INDEX2].transfer(regular_user, sell_amounts[1], {'from': deployer})

    token_balance_before = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    eth_balance_before = regular_user.balance()
    index1_balance_before = tokens[TOKEN_INDEX1].balanceOf(regular_user)
    index2_balance_before = tokens[TOKEN_INDEX2].balanceOf(regular_user)

    tokens[TOKEN_INDEX1].approve(indices_savings_swap.address, sell_amounts[0], {'from': regular_user})
    tokens[TOKEN_INDEX2].approve(indices_savings_swap.address, sell_amounts[1], {'from': regular_user})

    paths = [
        [tokens[TOKEN_INDEX1].address, tokens[TOKEN_TOKEN1].address],
        [tokens[TOKEN_INDEX2].address, tokens[TOKEN_WETH].address]
    ]
    indices_savings_swap.sell['address[],address[],uint[],uint[],address[][]'](
        [tokens[TOKEN_INDEX1].address, tokens[TOKEN_INDEX2].address],
        [tokens[TOKEN_TOKEN1].address, ETH_ADDRESS],
        sell_amounts,
        sell_amounts_out_min,
        paths,
        {'from': regular_user}
        )

    token_balance_after = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    eth_balance_after = regular_user.balance()
    index1_balance_after = tokens[TOKEN_INDEX1].balanceOf(regular_user)
    index2_balance_after = tokens[TOKEN_INDEX2].balanceOf(regular_user)

    assert index1_balance_before - index1_balance_after == sell_amounts[0]
    assert token_balance_after - token_balance_before >= sell_amounts_out_min[0]
    assert index2_balance_before - index2_balance_after == sell_amounts[1]
    assert eth_balance_after - eth_balance_before >= sell_amounts_out_min[1] # fee for tx can make error


def test_buy_zero(indices_savings_swap, tokens, uniswap_router, regular_user, deployer):
    path = [tokens[TOKEN_TOKEN1].address, tokens[TOKEN_INDEX1].address]
    with brownie.reverts(revert_pattern = "Swap zero amount"):
        indices_savings_swap.buy['address,address,uint,uint,address[]'](
            tokens[TOKEN_INDEX1].address,
            tokens[TOKEN_TOKEN1].address,
            0,
            0,
            path,
            {'from': regular_user}
            )

def test_sell_zero(indices_savings_swap, tokens, uniswap_router, regular_user, deployer):
    path = [tokens[TOKEN_INDEX1].address, tokens[TOKEN_TOKEN1].address]
    with brownie.reverts(revert_pattern = "Swap zero amount"):
        indices_savings_swap.sell['address,address,uint,uint,address[]'](
            tokens[TOKEN_INDEX1].address,
            tokens[TOKEN_TOKEN1].address,
            0,
            0,
            path,
            {'from': regular_user}
            )


def test_successful_buy_long_path(indices_savings_swap, tokens, uniswap_router, regular_user, deployer):
    buy_amount = amount_in_small_dimension(10, tokens[TOKEN_TOKEN1])
    buy_amount_out_min = uniswap_router.getAmountsOut(
        buy_amount,
        [tokens[TOKEN_TOKEN1].address, tokens[TOKEN_INDEX1].address]
     )[-1]
    assert buy_amount * 2 == buy_amount_out_min

    tokens[TOKEN_TOKEN1].transfer(regular_user, buy_amount, {'from': deployer})

    token_balance_before = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    index_balance_before = tokens[TOKEN_INDEX1].balanceOf(regular_user)

    tokens[TOKEN_TOKEN1].approve(indices_savings_swap.address, buy_amount, {'from': regular_user})

    path = [tokens[TOKEN_TOKEN1].address, tokens[TOKEN_TOKEN2].address, tokens[TOKEN_INDEX1].address]
    indices_savings_swap.buy['address,address,uint,uint,address[]'](
        tokens[TOKEN_INDEX1].address,
        tokens[TOKEN_TOKEN1].address,
        buy_amount,
        buy_amount_out_min,
        path,
        {'from': regular_user}
        )

    token_balance_after = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    index_balance_after = tokens[TOKEN_INDEX1].balanceOf(regular_user)

    assert buy_amount > 0
    assert buy_amount_out_min > 0
    assert token_balance_before - token_balance_after == buy_amount
    assert index_balance_after - index_balance_before >= buy_amount_out_min


def test_successful_sell_long_path(indices_savings_swap, tokens, uniswap_router, regular_user, deployer):
    sell_amount = amount_in_small_dimension(0.005, tokens[TOKEN_INDEX1])
    sell_amount_out_min = uniswap_router.getAmountsOut(
        sell_amount,
        [tokens[TOKEN_INDEX1].address, tokens[TOKEN_TOKEN1].address]
     )[-1]
    assert sell_amount / 2 == sell_amount_out_min

    tokens[TOKEN_INDEX1].transfer(regular_user, sell_amount, {'from': deployer})

    token_balance_before = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    index_balance_before = tokens[TOKEN_INDEX1].balanceOf(regular_user)

    tokens[TOKEN_INDEX1].approve(indices_savings_swap.address, sell_amount, {'from': regular_user})

    path = [tokens[TOKEN_INDEX1].address, tokens[TOKEN_TOKEN2].address, tokens[TOKEN_TOKEN1].address]
    indices_savings_swap.sell['address,address,uint,uint,address[]'](
        tokens[TOKEN_INDEX1].address,
        tokens[TOKEN_TOKEN1].address,
        sell_amount,
        sell_amount_out_min,
        path,
        {'from': regular_user}
        )

    token_balance_after = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    index_balance_after = tokens[TOKEN_INDEX1].balanceOf(regular_user)

    assert sell_amount > 0
    assert sell_amount_out_min > 0
    assert index_balance_before - index_balance_after == sell_amount
    assert token_balance_after - token_balance_before >= sell_amount_out_min

def test_buy_wrong_path(indices_savings_swap, tokens, uniswap_router, regular_user, deployer):
    buy_amount = amount_in_small_dimension(10, tokens[TOKEN_TOKEN1])
    buy_amount_out_min = uniswap_router.getAmountsOut(
        buy_amount,
        [tokens[TOKEN_TOKEN1].address, tokens[TOKEN_INDEX1].address]
     )[-1]

    tokens[TOKEN_TOKEN1].transfer(regular_user, buy_amount, {'from': deployer})
    tokens[TOKEN_TOKEN1].approve(indices_savings_swap.address, buy_amount, {'from': regular_user})

    path = [tokens[TOKEN_TOKEN1].address, tokens[TOKEN_TOKEN3].address, tokens[TOKEN_INDEX1].address]
    with brownie.reverts(revert_pattern = "mock wrong path"):
        indices_savings_swap.buy['address,address,uint,uint,address[]'](
            tokens[TOKEN_INDEX1].address,
            tokens[TOKEN_TOKEN1].address,
            buy_amount,
            buy_amount_out_min,
            path,
            {'from': regular_user}
            )


def test_sell_wrong_path(indices_savings_swap, tokens, uniswap_router, regular_user, deployer):
    sell_amount = amount_in_small_dimension(0.005, tokens[TOKEN_INDEX1])
    sell_amount_out_min = uniswap_router.getAmountsOut(
        sell_amount,
        [tokens[TOKEN_INDEX1].address, tokens[TOKEN_TOKEN1].address]
     )[-1]
    assert sell_amount / 2 == sell_amount_out_min

    tokens[TOKEN_INDEX1].transfer(regular_user, sell_amount, {'from': deployer})

    token_balance_before = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    index_balance_before = tokens[TOKEN_INDEX1].balanceOf(regular_user)

    tokens[TOKEN_INDEX1].approve(indices_savings_swap.address, sell_amount, {'from': regular_user})

    path = [tokens[TOKEN_INDEX1].address, tokens[TOKEN_TOKEN3].address, tokens[TOKEN_TOKEN1].address]
    with brownie.reverts(revert_pattern = "mock wrong path"):
        indices_savings_swap.sell['address,address,uint,uint,address[]'](
            tokens[TOKEN_INDEX1].address,
            tokens[TOKEN_TOKEN1].address,
            sell_amount,
            sell_amount_out_min,
            path,
            {'from': regular_user}
            )



def test_successful_sell_eth(indices_savings_swap, tokens, uniswap_router, regular_user, deployer):
    sell_amount = amount_in_small_dimension(0.1, tokens[TOKEN_INDEX1])
    sell_amount_out_min = uniswap_router.getAmountsOut(
        sell_amount,
        [tokens[TOKEN_INDEX1].address, tokens[TOKEN_WETH].address]
     )[-1]
    assert sell_amount / 1000000 == sell_amount_out_min
    assert tokens[TOKEN_WETH].balance() >= sell_amount_out_min

    tokens[TOKEN_INDEX1].transfer(regular_user, sell_amount, {'from': deployer})

    index_balance_before = tokens[TOKEN_INDEX1].balanceOf(regular_user)
    eth_balance_before = regular_user.balance()

    tokens[TOKEN_INDEX1].approve(indices_savings_swap.address, sell_amount, {'from': regular_user})

    path = [tokens[TOKEN_INDEX1].address, tokens[TOKEN_WETH].address]
    indices_savings_swap.sell['address,address,uint,uint,address[]'](
        tokens[TOKEN_INDEX1].address,
        ETH_ADDRESS,
        sell_amount,
        sell_amount_out_min,
        path,
        {'from': regular_user}
        )

    index_balance_after = tokens[TOKEN_INDEX1].balanceOf(regular_user)
    eth_balance_after = regular_user.balance()

    assert sell_amount > 0
    assert sell_amount_out_min > 0
    assert index_balance_before - index_balance_after == sell_amount
    assert eth_balance_after - eth_balance_before >= sell_amount_out_min # fee for tx can make error


def test_multiple_purchases_with_broken_record(indices_savings_swap, tokens, uniswap_router, uniswap_router2, regular_user, deployer):
    buy_amounts = [
        amount_in_small_dimension(10, tokens[TOKEN_TOKEN1]),
        int(1 * (10 ** WETH_DECIMALS) / 50000)
    ]
    buy_amounts_out_min = [
         uniswap_router.getAmountsOut(
                buy_amounts[0],
                [tokens[TOKEN_TOKEN1].address, tokens[TOKEN_INDEX1].address]
             )[-1],
         uniswap_router2.getAmountsOut(
                 buy_amounts[1],
                 [tokens[TOKEN_WETH].address, tokens[TOKEN_INDEX2].address]
              )[-1]
    ]
    assert buy_amounts[0] * 2 == buy_amounts_out_min[0]
    assert buy_amounts[1] * 1000000 == buy_amounts_out_min[1]

    tokens[TOKEN_TOKEN1].transfer(regular_user, buy_amounts[0], {'from': deployer})

    token_balance_before = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    eth_balance_before = regular_user.balance()
    index1_balance_before = tokens[TOKEN_INDEX1].balanceOf(regular_user)
    index2_balance_before = tokens[TOKEN_INDEX2].balanceOf(regular_user)

    assert buy_amounts[0] <= token_balance_before
    assert buy_amounts[1] <= eth_balance_before

    tokens[TOKEN_TOKEN1].approve(indices_savings_swap.address, buy_amounts[0], {'from': regular_user})

    paths = [
        [tokens[TOKEN_TOKEN1].address, tokens[TOKEN_INDEX1].address],
        [tokens[TOKEN_WETH].address, tokens[TOKEN_INDEX3].address, tokens[TOKEN_INDEX2].address]
    ]
    with brownie.reverts(revert_pattern = "mock wrong path"):
        indices_savings_swap.buy['address[],address[],uint[],uint[],address[][]'](
            [tokens[TOKEN_INDEX1].address, tokens[TOKEN_INDEX2].address],
            [tokens[TOKEN_TOKEN1].address, ETH_ADDRESS],
            buy_amounts,
            buy_amounts_out_min,
            paths,
            {'from': regular_user, "value": str(buy_amounts[1]) + " wei" }
            )

    token_balance_after = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    eth_balance_after = regular_user.balance()
    index1_balance_after = tokens[TOKEN_INDEX1].balanceOf(regular_user)
    index2_balance_after = tokens[TOKEN_INDEX2].balanceOf(regular_user)

    assert token_balance_before == token_balance_after
    assert eth_balance_before <= eth_balance_after  # fee for tx can make error
    assert index1_balance_after == index1_balance_before
    assert index2_balance_after == index2_balance_before


def test_multiple_sales_with_broken_record(indices_savings_swap, tokens, uniswap_router, uniswap_router2, regular_user, deployer):
    sell_amounts = [
        amount_in_small_dimension(0.005, tokens[TOKEN_INDEX1]),
        amount_in_small_dimension(0.1, tokens[TOKEN_INDEX2])
    ]
    sell_amounts_out_min = [
        uniswap_router.getAmountsOut(
                sell_amounts[0],
                [tokens[TOKEN_INDEX1].address, tokens[TOKEN_TOKEN1].address]
             )[-1],
        uniswap_router2.getAmountsOut(
                sell_amounts[1],
                [tokens[TOKEN_INDEX2].address, tokens[TOKEN_WETH].address]
             )[-1]
    ]
    assert sell_amounts[0] / 2 == sell_amounts_out_min[0]
    assert sell_amounts[1] / 1000000 == sell_amounts_out_min[1]

    tokens[TOKEN_INDEX1].transfer(regular_user, sell_amounts[0], {'from': deployer})
    tokens[TOKEN_INDEX2].transfer(regular_user, sell_amounts[1], {'from': deployer})

    token_balance_before = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    eth_balance_before = regular_user.balance()
    index1_balance_before = tokens[TOKEN_INDEX1].balanceOf(regular_user)
    index2_balance_before = tokens[TOKEN_INDEX2].balanceOf(regular_user)

    tokens[TOKEN_INDEX1].approve(indices_savings_swap.address, sell_amounts[0], {'from': regular_user})
    tokens[TOKEN_INDEX2].approve(indices_savings_swap.address, sell_amounts[1], {'from': regular_user})

    paths = [
        [tokens[TOKEN_INDEX1].address, tokens[TOKEN_TOKEN1].address],
        [tokens[TOKEN_INDEX2].address, tokens[TOKEN_INDEX3].address, tokens[TOKEN_WETH].address]
    ]
    with brownie.reverts(revert_pattern = "mock wrong path"):
        indices_savings_swap.sell['address[],address[],uint[],uint[],address[][]'](
            [tokens[TOKEN_INDEX1].address, tokens[TOKEN_INDEX2].address],
            [tokens[TOKEN_TOKEN1].address, ETH_ADDRESS],
            sell_amounts,
            sell_amounts_out_min,
            paths,
            {'from': regular_user}
            )

    token_balance_after = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    eth_balance_after = regular_user.balance()
    index1_balance_after = tokens[TOKEN_INDEX1].balanceOf(regular_user)
    index2_balance_after = tokens[TOKEN_INDEX2].balanceOf(regular_user)

    assert token_balance_before == token_balance_after
    assert eth_balance_before <= eth_balance_after  # fee for tx can make error
    assert index1_balance_after == index1_balance_before
    assert index2_balance_after == index2_balance_before


def test_buy_with_wrong_out_min(indices_savings_swap, tokens, uniswap_router, regular_user, deployer):
    buy_amount = amount_in_small_dimension(10, tokens[TOKEN_TOKEN1])
    buy_amount_out_min = 10 ** 50

    tokens[TOKEN_TOKEN1].transfer(regular_user, buy_amount, {'from': deployer})

    token_balance_before = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    index_balance_before = tokens[TOKEN_INDEX1].balanceOf(regular_user)

    tokens[TOKEN_TOKEN1].approve(indices_savings_swap.address, buy_amount, {'from': regular_user})

    path = [tokens[TOKEN_TOKEN1].address, tokens[TOKEN_INDEX1].address]
    with brownie.reverts(revert_pattern = "mock small price"):
        indices_savings_swap.buy['address,address,uint,uint,address[]'](
            tokens[TOKEN_INDEX1].address,
            tokens[TOKEN_TOKEN1].address,
            buy_amount,
            buy_amount_out_min,
            path,
            {'from': regular_user}
            )

    token_balance_after = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    index_balance_after = tokens[TOKEN_INDEX1].balanceOf(regular_user)

    assert token_balance_before == token_balance_after
    assert index_balance_after == index_balance_before


def test_sell_with_wrong_out_min(indices_savings_swap, tokens, uniswap_router, regular_user, deployer):
    sell_amount = amount_in_small_dimension(0.005, tokens[TOKEN_INDEX1])
    sell_amount_out_min = 10 ** 50

    tokens[TOKEN_INDEX1].transfer(regular_user, sell_amount, {'from': deployer})

    token_balance_before = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    index_balance_before = tokens[TOKEN_INDEX1].balanceOf(regular_user)

    tokens[TOKEN_INDEX1].approve(indices_savings_swap.address, sell_amount, {'from': regular_user})

    path = [tokens[TOKEN_INDEX1].address, tokens[TOKEN_TOKEN1].address]
    with brownie.reverts(revert_pattern = "mock small price"):
        indices_savings_swap.sell['address,address,uint,uint,address[]'](
            tokens[TOKEN_INDEX1].address,
            tokens[TOKEN_TOKEN1].address,
            sell_amount,
            sell_amount_out_min,
            path,
            {'from': regular_user}
            )

    token_balance_after = tokens[TOKEN_TOKEN1].balanceOf(regular_user)
    index_balance_after = tokens[TOKEN_INDEX1].balanceOf(regular_user)

    assert token_balance_before == token_balance_after
    assert index_balance_after == index_balance_before