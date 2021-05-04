import pytest
import brownie

from constants import *
from utils.utils import amount_in_small_dimension


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_successful_buy(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    buy_amount = amount_in_small_dimension(10, tokens[TOKEN_USDT])
    buy_amount_out_min = sushi_router.getAmountsOut(
        buy_amount,
        [tokens[TOKEN_USDT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_PIPT].address]
     )[-1]

    tokens[TOKEN_USDT].transfer(regular_user, buy_amount, {'from': deployer})

    token_balance_before = tokens[TOKEN_USDT].balanceOf(regular_user)
    index_balance_before = tokens[TOKEN_PIPT].balanceOf(regular_user)

    tokens[TOKEN_USDT].approve(indices_savings_swap.address, buy_amount, {'from': regular_user})

    path = [tokens[TOKEN_USDT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_PIPT].address]
    indices_savings_swap.buy['address,address,uint,uint,address[]'](
        tokens[TOKEN_PIPT].address,
        tokens[TOKEN_USDT].address,
        buy_amount,
        buy_amount_out_min,
        path,
        {'from': regular_user}
        )

    token_balance_after = tokens[TOKEN_USDT].balanceOf(regular_user)
    index_balance_after = tokens[TOKEN_PIPT].balanceOf(regular_user)

    assert buy_amount > 0
    assert buy_amount_out_min > 0
    assert token_balance_before - token_balance_after == buy_amount
    assert index_balance_after - index_balance_before >= buy_amount_out_min


def test_successful_sell(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    sell_amount = amount_in_small_dimension(0.005, tokens[TOKEN_PIPT])
    sell_amount_out_min = sushi_router.getAmountsOut(
        sell_amount,
        [tokens[TOKEN_PIPT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_USDT].address]
     )[-1]

    tokens[TOKEN_PIPT].transfer(regular_user, sell_amount, {'from': deployer})

    token_balance_before = tokens[TOKEN_USDT].balanceOf(regular_user)
    index_balance_before = tokens[TOKEN_PIPT].balanceOf(regular_user)

    tokens[TOKEN_PIPT].approve(indices_savings_swap.address, sell_amount, {'from': regular_user})

    path = [tokens[TOKEN_PIPT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_USDT].address]
    indices_savings_swap.sell['address,address,uint,uint,address[]'](
        tokens[TOKEN_PIPT].address,
        tokens[TOKEN_USDT].address,
        sell_amount,
        sell_amount_out_min,
        path,
        {'from': regular_user}
        )

    token_balance_after = tokens[TOKEN_USDT].balanceOf(regular_user)
    index_balance_after = tokens[TOKEN_PIPT].balanceOf(regular_user)

    assert sell_amount > 0
    assert sell_amount_out_min > 0
    assert index_balance_before - index_balance_after == sell_amount
    assert token_balance_after - token_balance_before >= sell_amount_out_min


def test_successful_buy_eth(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    buy_amount = int(1 * (10 ** WETH_DECIMALS) / 50000)
    buy_amount_out_min = sushi_router.getAmountsOut(
        buy_amount,
        [tokens[TOKEN_WETH].address, tokens[TOKEN_PIPT].address]
     )[-1]

    eth_balance_before = regular_user.balance()
    index_balance_before = tokens[TOKEN_PIPT].balanceOf(regular_user)
    assert buy_amount < eth_balance_before

    path = [tokens[TOKEN_WETH].address, tokens[TOKEN_PIPT].address]
    indices_savings_swap.buy['address,address,uint,uint,address[]'](
        tokens[TOKEN_PIPT].address,
        ETH_ADDRESS,
        buy_amount,
        buy_amount_out_min,
        path,
        {'from': regular_user, "value": str(buy_amount) + " wei" }
        )

    eth_balance_after = regular_user.balance()
    index_balance_after = tokens[TOKEN_PIPT].balanceOf(regular_user)

    assert buy_amount > 0
    assert buy_amount_out_min > 0
    assert eth_balance_before - eth_balance_after >= buy_amount # fee for tx can make error
    assert index_balance_after - index_balance_before >= buy_amount_out_min


def test_successful_sell_eth(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    sell_amount = amount_in_small_dimension(0.1, tokens[TOKEN_PIPT])
    sell_amount_out_min = sushi_router.getAmountsOut(
        sell_amount,
        [tokens[TOKEN_PIPT].address, tokens[TOKEN_WETH].address]
     )[-1]

    tokens[TOKEN_PIPT].transfer(regular_user, sell_amount, {'from': deployer})

    index_balance_before = tokens[TOKEN_PIPT].balanceOf(regular_user)
    eth_balance_before = regular_user.balance()

    tokens[TOKEN_PIPT].approve(indices_savings_swap.address, sell_amount, {'from': regular_user})

    path = [tokens[TOKEN_PIPT].address, tokens[TOKEN_WETH].address]
    indices_savings_swap.sell['address,address,uint,uint,address[]'](
        tokens[TOKEN_PIPT].address,
        ETH_ADDRESS,
        sell_amount,
        sell_amount_out_min,
        path,
        {'from': regular_user}
        )

    index_balance_after = tokens[TOKEN_PIPT].balanceOf(regular_user)
    eth_balance_after = regular_user.balance()

    assert sell_amount > 0
    assert sell_amount_out_min > 0
    assert index_balance_before - index_balance_after == sell_amount
    assert eth_balance_after - eth_balance_before >= sell_amount_out_min # fee for tx can make error


def test_successful_multiple_purchases(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    buy_amounts = [
        amount_in_small_dimension(10, tokens[TOKEN_USDC]),
        int(1 * (10 ** WETH_DECIMALS) / 50000)
    ]
    buy_amounts_out_min = [
         sushi_router.getAmountsOut(
                buy_amounts[0],
                [tokens[TOKEN_USDC].address, tokens[TOKEN_YLA].address]
             )[-1],
         sushi_router.getAmountsOut(
                 buy_amounts[1],
                 [tokens[TOKEN_WETH].address, tokens[TOKEN_ASSY].address]
              )[-1]
    ]

    tokens[TOKEN_USDC].transfer(regular_user, buy_amounts[0], {'from': deployer})

    token_balance_before = tokens[TOKEN_USDC].balanceOf(regular_user)
    eth_balance_before = regular_user.balance()
    index1_balance_before = tokens[TOKEN_YLA].balanceOf(regular_user)
    index2_balance_before = tokens[TOKEN_ASSY].balanceOf(regular_user)

    assert buy_amounts[0] <= token_balance_before
    assert buy_amounts[1] <= eth_balance_before

    tokens[TOKEN_USDC].approve(indices_savings_swap.address, buy_amounts[0], {'from': regular_user})

    paths = [
        [tokens[TOKEN_USDC].address, tokens[TOKEN_YLA].address],
        [tokens[TOKEN_WETH].address, tokens[TOKEN_ASSY].address]
    ]
    indices_savings_swap.buy['address[],address[],uint[],uint[],address[][]'](
        [tokens[TOKEN_YLA].address, tokens[TOKEN_ASSY].address],
        [tokens[TOKEN_USDC].address, ETH_ADDRESS],
        buy_amounts,
        buy_amounts_out_min,
        paths,
        {'from': regular_user, "value": str(buy_amounts[1]) + " wei" }
        )

    token_balance_after = tokens[TOKEN_USDC].balanceOf(regular_user)
    eth_balance_after = regular_user.balance()
    index1_balance_after = tokens[TOKEN_YLA].balanceOf(regular_user)
    index2_balance_after = tokens[TOKEN_ASSY].balanceOf(regular_user)

    assert token_balance_before - token_balance_after == buy_amounts[0]
    assert eth_balance_before - eth_balance_after >= buy_amounts[1] # fee for tx can make error
    assert index1_balance_after - index1_balance_before >= buy_amounts_out_min[0]
    assert index2_balance_after - index2_balance_before >= buy_amounts_out_min[1]


def test_successful_multiple_sales(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    sell_amounts = [
        amount_in_small_dimension(0.005, tokens[TOKEN_YLA]),
        amount_in_small_dimension(0.1, tokens[TOKEN_ASSY])
    ]
    sell_amounts_out_min = [
        sushi_router.getAmountsOut(
                sell_amounts[0],
                [tokens[TOKEN_YLA].address, tokens[TOKEN_USDC].address]
             )[-1],
        sushi_router.getAmountsOut(
                sell_amounts[1],
                [tokens[TOKEN_ASSY].address, tokens[TOKEN_WETH].address]
             )[-1]
    ]

    tokens[TOKEN_YLA].transfer(regular_user, sell_amounts[0], {'from': deployer})
    tokens[TOKEN_ASSY].transfer(regular_user, sell_amounts[1], {'from': deployer})

    token_balance_before = tokens[TOKEN_USDC].balanceOf(regular_user)
    eth_balance_before = regular_user.balance()
    index1_balance_before = tokens[TOKEN_YLA].balanceOf(regular_user)
    index2_balance_before = tokens[TOKEN_ASSY].balanceOf(regular_user)

    tokens[TOKEN_YLA].approve(indices_savings_swap.address, sell_amounts[0], {'from': regular_user})
    tokens[TOKEN_ASSY].approve(indices_savings_swap.address, sell_amounts[1], {'from': regular_user})

    paths = [
        [tokens[TOKEN_YLA].address, tokens[TOKEN_USDC].address],
        [tokens[TOKEN_ASSY].address, tokens[TOKEN_WETH].address]
    ]
    indices_savings_swap.sell['address[],address[],uint[],uint[],address[][]'](
        [tokens[TOKEN_YLA].address, tokens[TOKEN_ASSY].address],
        [tokens[TOKEN_USDC].address, ETH_ADDRESS],
        sell_amounts,
        sell_amounts_out_min,
        paths,
        {'from': regular_user}
        )

    token_balance_after = tokens[TOKEN_USDC].balanceOf(regular_user)
    eth_balance_after = regular_user.balance()
    index1_balance_after = tokens[TOKEN_YLA].balanceOf(regular_user)
    index2_balance_after = tokens[TOKEN_ASSY].balanceOf(regular_user)

    assert index1_balance_before - index1_balance_after == sell_amounts[0]
    assert token_balance_after - token_balance_before >= sell_amounts_out_min[0]
    assert index2_balance_before - index2_balance_after == sell_amounts[1]
    assert eth_balance_after - eth_balance_before >= sell_amounts_out_min[1] # fee for tx can make error


def test_buy_zero(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    path = [tokens[TOKEN_USDT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_PIPT].address]
    with brownie.reverts():
        indices_savings_swap.buy['address,address,uint,uint,address[]'](
            tokens[TOKEN_PIPT].address,
            tokens[TOKEN_USDT].address,
            0,
            0,
            path,
            {'from': regular_user}
            )

def test_sell_zero(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    path = [tokens[TOKEN_PIPT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_USDT].address]
    with brownie.reverts():
        indices_savings_swap.sell['address,address,uint,uint,address[]'](
            tokens[TOKEN_PIPT].address,
            tokens[TOKEN_USDT].address,
            0,
            0,
            path,
            {'from': regular_user}
            )


def test_successful_buy_long_path(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    buy_amount = amount_in_small_dimension(10, tokens[TOKEN_USDT])
    buy_amount_out_min = sushi_router.getAmountsOut(
        buy_amount,
        [tokens[TOKEN_USDT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_YETI].address]
     )[-1]

    tokens[TOKEN_USDT].transfer(regular_user, buy_amount, {'from': deployer})

    token_balance_before = tokens[TOKEN_USDT].balanceOf(regular_user)
    index_balance_before = tokens[TOKEN_YETI].balanceOf(regular_user)

    tokens[TOKEN_USDT].approve(indices_savings_swap.address, buy_amount, {'from': regular_user})

    path = [tokens[TOKEN_USDT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_YETI].address]
    indices_savings_swap.buy['address,address,uint,uint,address[]'](
        tokens[TOKEN_YETI].address,
        tokens[TOKEN_USDT].address,
        buy_amount,
        buy_amount_out_min,
        path,
        {'from': regular_user}
        )

    token_balance_after = tokens[TOKEN_USDT].balanceOf(regular_user)
    index_balance_after = tokens[TOKEN_YETI].balanceOf(regular_user)

    assert buy_amount > 0
    assert buy_amount_out_min > 0
    assert token_balance_before - token_balance_after == buy_amount
    assert index_balance_after - index_balance_before >= buy_amount_out_min


def test_successful_sell_long_path(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    sell_amount = amount_in_small_dimension(0.005, tokens[TOKEN_PIPT])
    sell_amount_out_min = sushi_router.getAmountsOut(
        sell_amount,
        [tokens[TOKEN_PIPT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_USDT].address]
     )[-1]

    tokens[TOKEN_PIPT].transfer(regular_user, sell_amount, {'from': deployer})

    token_balance_before = tokens[TOKEN_USDT].balanceOf(regular_user)
    index_balance_before = tokens[TOKEN_PIPT].balanceOf(regular_user)

    tokens[TOKEN_PIPT].approve(indices_savings_swap.address, sell_amount, {'from': regular_user})

    path = [tokens[TOKEN_PIPT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_USDT].address]
    indices_savings_swap.sell['address,address,uint,uint,address[]'](
        tokens[TOKEN_PIPT].address,
        tokens[TOKEN_USDT].address,
        sell_amount,
        sell_amount_out_min,
        path,
        {'from': regular_user}
        )

    token_balance_after = tokens[TOKEN_USDT].balanceOf(regular_user)
    index_balance_after = tokens[TOKEN_PIPT].balanceOf(regular_user)

    assert sell_amount > 0
    assert sell_amount_out_min > 0
    assert index_balance_before - index_balance_after == sell_amount
    assert token_balance_after - token_balance_before >= sell_amount_out_min


def test_buy_wrong_path(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    buy_amount = amount_in_small_dimension(10, tokens[TOKEN_USDT])
    buy_amount_out_min = sushi_router.getAmountsOut(
        buy_amount,
        [tokens[TOKEN_USDT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_PIPT].address]
     )[-1]

    tokens[TOKEN_USDT].transfer(regular_user, buy_amount, {'from': deployer})
    tokens[TOKEN_USDT].approve(indices_savings_swap.address, buy_amount, {'from': regular_user})

    path = [tokens[TOKEN_USDT].address, tokens[TOKEN_PIPT].address]
    with brownie.reverts():
        indices_savings_swap.buy['address,address,uint,uint,address[]'](
            tokens[TOKEN_PIPT].address,
            tokens[TOKEN_USDT].address,
            buy_amount,
            buy_amount_out_min,
            path,
            {'from': regular_user}
            )


def test_sell_wrong_path(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    sell_amount = amount_in_small_dimension(0.005, tokens[TOKEN_PIPT])
    sell_amount_out_min = sushi_router.getAmountsOut(
        sell_amount,
        [tokens[TOKEN_PIPT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_USDT].address]
     )[-1]

    tokens[TOKEN_PIPT].transfer(regular_user, sell_amount, {'from': deployer})

    token_balance_before = tokens[TOKEN_USDT].balanceOf(regular_user)
    index_balance_before = tokens[TOKEN_PIPT].balanceOf(regular_user)

    tokens[TOKEN_PIPT].approve(indices_savings_swap.address, sell_amount, {'from': regular_user})

    path = [tokens[TOKEN_PIPT].address, tokens[TOKEN_USDT].address]
    with brownie.reverts():
        indices_savings_swap.sell['address,address,uint,uint,address[]'](
            tokens[TOKEN_PIPT].address,
            tokens[TOKEN_USDT].address,
            sell_amount,
            sell_amount_out_min,
            path,
            {'from': regular_user}
            )


def test_successful_sell_eth(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    sell_amount = amount_in_small_dimension(0.1, tokens[TOKEN_PIPT])
    sell_amount_out_min = sushi_router.getAmountsOut(
        sell_amount,
        [tokens[TOKEN_YLA].address, tokens[TOKEN_USDC].address, tokens[TOKEN_WETH].address]
     )[-1]

    tokens[TOKEN_YLA].transfer(regular_user, sell_amount, {'from': deployer})

    index_balance_before = tokens[TOKEN_YLA].balanceOf(regular_user)
    eth_balance_before = regular_user.balance()

    tokens[TOKEN_YLA].approve(indices_savings_swap.address, sell_amount, {'from': regular_user})

    path = [tokens[TOKEN_YLA].address, tokens[TOKEN_USDC].address, tokens[TOKEN_WETH].address]
    indices_savings_swap.sell['address,address,uint,uint,address[]'](
        tokens[TOKEN_YLA].address,
        ETH_ADDRESS,
        sell_amount,
        sell_amount_out_min,
        path,
        {'from': regular_user}
        )

    index_balance_after = tokens[TOKEN_PIPT].balanceOf(regular_user)
    eth_balance_after = regular_user.balance()

    assert sell_amount > 0
    assert sell_amount_out_min > 0
    assert index_balance_before - index_balance_after == sell_amount
    assert eth_balance_after - eth_balance_before >= sell_amount_out_min # fee for tx can make error


def test_multiple_purchases_with_broken_record(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    buy_amounts = [
        amount_in_small_dimension(10, tokens[TOKEN_USDT]),
        int(1 * (10 ** WETH_DECIMALS) / 50000)
    ]
    buy_amounts_out_min = [
         sushi_router.getAmountsOut(
                buy_amounts[0],
                [tokens[TOKEN_USDT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_PIPT].address]
             )[-1],
         sushi_router.getAmountsOut(
                 buy_amounts[1],
                 [tokens[TOKEN_WETH].address, tokens[TOKEN_USDC].address, tokens[TOKEN_YLA].address]
              )[-1]
    ]

    tokens[TOKEN_USDT].transfer(regular_user, buy_amounts[0], {'from': deployer})

    token_balance_before = tokens[TOKEN_USDT].balanceOf(regular_user)
    eth_balance_before = regular_user.balance()
    index1_balance_before = tokens[TOKEN_PIPT].balanceOf(regular_user)
    index2_balance_before = tokens[TOKEN_YLA].balanceOf(regular_user)

    assert buy_amounts[0] <= token_balance_before
    assert buy_amounts[1] <= eth_balance_before

    tokens[TOKEN_USDT].approve(indices_savings_swap.address, buy_amounts[0], {'from': regular_user})

    paths = [
        [tokens[TOKEN_USDT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_PIPT].address],
        [tokens[TOKEN_WETH].address, tokens[TOKEN_USDT].address, tokens[TOKEN_YLA].address] # TOKEN_USDT wrong
    ]
    with brownie.reverts():
        indices_savings_swap.buy['address[],address[],uint[],uint[],address[][]'](
            [tokens[TOKEN_PIPT].address, tokens[TOKEN_YLA].address],
            [tokens[TOKEN_USDT].address, ETH_ADDRESS],
            buy_amounts,
            buy_amounts_out_min,
            paths,
            {'from': regular_user, "value": str(buy_amounts[1]) + " wei" }
            )

    token_balance_after = tokens[TOKEN_USDT].balanceOf(regular_user)
    eth_balance_after = regular_user.balance()
    index1_balance_after = tokens[TOKEN_PIPT].balanceOf(regular_user)
    index2_balance_after = tokens[TOKEN_YLA].balanceOf(regular_user)

    assert token_balance_before == token_balance_after
    assert eth_balance_before <= eth_balance_after  # fee for tx can make error
    assert index1_balance_after == index1_balance_before
    assert index2_balance_after == index2_balance_before


def test_multiple_sales_with_broken_record(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    sell_amounts = [
        amount_in_small_dimension(0.005, tokens[TOKEN_PIPT]),
        amount_in_small_dimension(0.1, tokens[TOKEN_ASSY])
    ]
    sell_amounts_out_min = [
        sushi_router.getAmountsOut(
                sell_amounts[0],
                [tokens[TOKEN_PIPT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_USDT].address]
             )[-1],
        sushi_router.getAmountsOut(
                sell_amounts[1],
                [tokens[TOKEN_YLA].address, tokens[TOKEN_USDC].address, tokens[TOKEN_WETH].address]
             )[-1]
    ]

    tokens[TOKEN_PIPT].transfer(regular_user, sell_amounts[0], {'from': deployer})
    tokens[TOKEN_YLA].transfer(regular_user, sell_amounts[1], {'from': deployer})

    token_balance_before = tokens[TOKEN_USDT].balanceOf(regular_user)
    eth_balance_before = regular_user.balance()
    index1_balance_before = tokens[TOKEN_PIPT].balanceOf(regular_user)
    index2_balance_before = tokens[TOKEN_YLA].balanceOf(regular_user)

    tokens[TOKEN_PIPT].approve(indices_savings_swap.address, sell_amounts[0], {'from': regular_user})
    tokens[TOKEN_YLA].approve(indices_savings_swap.address, sell_amounts[1], {'from': regular_user})

    paths = [
        [tokens[TOKEN_PIPT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_USDT].address],
        [tokens[TOKEN_YLA].address, tokens[TOKEN_USDT].address, tokens[TOKEN_WETH].address]
    ]
    with brownie.reverts():
        indices_savings_swap.sell['address[],address[],uint[],uint[],address[][]'](
            [tokens[TOKEN_PIPT].address, tokens[TOKEN_YLA].address],
            [tokens[TOKEN_USDT].address, ETH_ADDRESS],
            sell_amounts,
            sell_amounts_out_min,
            paths,
            {'from': regular_user}
            )

    token_balance_after = tokens[TOKEN_USDT].balanceOf(regular_user)
    eth_balance_after = regular_user.balance()
    index1_balance_after = tokens[TOKEN_PIPT].balanceOf(regular_user)
    index2_balance_after = tokens[TOKEN_YLA].balanceOf(regular_user)

    assert token_balance_before == token_balance_after
    assert eth_balance_before <= eth_balance_after  # fee for tx can make error
    assert index1_balance_after == index1_balance_before
    assert index2_balance_after == index2_balance_before


def test_buy_with_wrong_out_min(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    buy_amount = amount_in_small_dimension(10, tokens[TOKEN_USDT])
    buy_amount_out_min = 10 ** 50

    tokens[TOKEN_USDT].transfer(regular_user, buy_amount, {'from': deployer})

    token_balance_before = tokens[TOKEN_USDT].balanceOf(regular_user)
    index_balance_before = tokens[TOKEN_PIPT].balanceOf(regular_user)

    tokens[TOKEN_USDT].approve(indices_savings_swap.address, buy_amount, {'from': regular_user})

    path = [tokens[TOKEN_USDT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_PIPT].address]
    with brownie.reverts():
        indices_savings_swap.buy['address,address,uint,uint,address[]'](
            tokens[TOKEN_PIPT].address,
            tokens[TOKEN_USDT].address,
            buy_amount,
            buy_amount_out_min,
            path,
            {'from': regular_user}
            )

    token_balance_after = tokens[TOKEN_USDT].balanceOf(regular_user)
    index_balance_after = tokens[TOKEN_PIPT].balanceOf(regular_user)

    assert token_balance_before == token_balance_after
    assert index_balance_after == index_balance_before


def test_sell_with_wrong_out_min(indices_savings_swap, tokens, sushi_router, regular_user, deployer):
    sell_amount = amount_in_small_dimension(0.005, tokens[TOKEN_PIPT])
    sell_amount_out_min = 10 ** 50

    tokens[TOKEN_PIPT].transfer(regular_user, sell_amount, {'from': deployer})

    token_balance_before = tokens[TOKEN_USDT].balanceOf(regular_user)
    index_balance_before = tokens[TOKEN_PIPT].balanceOf(regular_user)

    tokens[TOKEN_PIPT].approve(indices_savings_swap.address, sell_amount, {'from': regular_user})

    path = [tokens[TOKEN_PIPT].address, tokens[TOKEN_WETH].address, tokens[TOKEN_USDT].address]
    with brownie.reverts():
        indices_savings_swap.sell['address,address,uint,uint,address[]'](
            tokens[TOKEN_PIPT].address,
            tokens[TOKEN_USDT].address,
            sell_amount,
            sell_amount_out_min,
            path,
            {'from': regular_user}
            )

    token_balance_after = tokens[TOKEN_USDT].balanceOf(regular_user)
    index_balance_after = tokens[TOKEN_PIPT].balanceOf(regular_user)

    assert token_balance_before == token_balance_after
    assert index_balance_after == index_balance_before