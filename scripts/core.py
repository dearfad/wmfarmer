import pandas as pd

def item_price(orders):
    orders_df = pd.json_normalize(orders)
    item_price = {
        'ingame_highest_buy_platinum': 0,
        'ingame_lowest_sell_platinum': 0,
    }

    # ingame_hightest_buy
    ingame_buy_orders = orders_df[(orders_df['user.status'] == 'ingame') & (
        orders_df['order_type'] == 'buy')].sort_values(by='platinum', ascending=False)
    if not ingame_buy_orders.empty:
        item_price['ingame_highest_buy_platinum'] = ingame_buy_orders.iloc[0].at['platinum']

    # ingame_lowest_sell
    ingame_sell_orders = orders_df[(orders_df['user.status'] == 'ingame') & (
        orders_df['order_type'] == 'sell')].sort_values(by='platinum', ascending=True)
    if not ingame_sell_orders.empty:
        item_price['ingame_lowest_sell_platinum'] = ingame_sell_orders.iloc[0].at['platinum']

    return item_price
