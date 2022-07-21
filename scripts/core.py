import streamlit as st
from scripts.wmmarket import item_orders, item_info
import numpy as np
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

@st.cache(show_spinner=False, suppress_st_warning=True, ttl=86400.0)
def get_warframe_price():

    warframe_prime_list = ['ash', 'atlas', 'banshee', 'chroma', 'ember', 'equinox', 'frost', 'gara', 'garuda', 'harrow', 'hydroid', 'inaros', 'ivara', 'khora', 'limbo', 'loki', 'mag',
                            'mesa', 'mirage', 'nekros', 'nezha', 'nidus', 'nova', 'nyx', 'oberon', 'octavia', 'rhino', 'saryn', 'titania', 'trinity', 'valkyr', 'vauban', 'volt', 'wukong', 'zephyr']
    warframe_prime_set_list = ['set', 'blueprint', 'neuroptics', 'chassis', 'systems']

    warframe_price_df = pd.DataFrame(data=np.zeros((len(warframe_prime_list),len(warframe_prime_set_list)), dtype = int), index=warframe_prime_list, columns=warframe_prime_set_list)

    progress = st.empty()

    for i, warframe in enumerate(warframe_prime_list):
        progress.write(f"🚴‍♂️ **{warframe.upper()}** ...")
        for item in warframe_prime_set_list:
            url_name = warframe + '_prime_' + item
            if warframe=='khora':
                if item in ['neuroptics', 'chassis', 'systems']:
                    url_name = url_name + '_blueprint'
            orders = item_orders(url_name)
            price = item_price(orders['orders'])
            info = item_info(url_name)


            ducats = int(info['info'].get('ducats', '--'))
            label = "💛" if ducats==100 else ""
    
            warframe_price_df.loc[warframe, item] = str(price['ingame_lowest_sell_platinum']).rjust(3) + '-' + str(price['ingame_highest_buy_platinum']).ljust(3) + label
    progress.empty()

    return warframe_price_df