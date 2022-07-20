import streamlit as st
import pandas as pd

def item_price(orders):
    orders_df = pd.json_normalize(orders)
    item_price = {
        'ingame_highest_buy_platinum': 0,
        'ingame_highest_buyer': '',
        'ingame_high_buy': pd.DataFrame(),
        'week_high_buy_platinum': 0,
        'ingame_lowest_sell_platinum': 0,
        'ingame_lowest_seller': '',
        'ingame_low_sell': pd.DataFrame(),
        'week_low_sell_platinum': 0,        
    }

    # ingame_hightest_buy
    ingame_buy_orders = orders_df[(orders_df['user.status'] == 'ingame') & (
        orders_df['order_type'] == 'buy')].sort_values(by='platinum', ascending=False)
    if not ingame_buy_orders.empty:
        item_price['ingame_highest_buy_platinum'] = ingame_buy_orders.iloc[0].at['platinum']
        item_price['ingame_highest_buyer'] = ingame_buy_orders.iloc[0].at['user.ingame_name']
        item_price['ingame_high_buy'] = ingame_buy_orders.head(5)
    # week_high_buy

    # ingame_lowest_sell
    ingame_sell_orders = orders_df[(orders_df['user.status'] == 'ingame') & (
        orders_df['order_type'] == 'sell')].sort_values(by='platinum', ascending=True)
    if not ingame_sell_orders.empty:
        item_price['ingame_lowest_sell_platinum'] = ingame_sell_orders.iloc[0].at['platinum']
        item_price['ingame_lowest_seller'] = ingame_sell_orders.iloc[0].at['user.ingame_name']
        item_price['ingame_low_sell'] = ingame_sell_orders.head(5)
    # week_low_sell

    return item_price
