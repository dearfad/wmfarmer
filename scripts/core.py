import streamlit as st
from scripts.wmmarket import get_item_orders, get_item_info
import numpy as np
import pandas as pd

def get_item_price(orders):
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
            item_orders = get_item_orders(url_name)
            item_price = get_item_price(item_orders['orders'])
            item_info = get_item_info(url_name)


            # ducats = int(info['info'].get('ducats', '--'))
            # label = "💛" if ducats==100 else ""    
            # warframe_price_df.loc[warframe, item] = str(item_price['ingame_lowest_sell_platinum']) + ' - ' + str(item_price['ingame_highest_buy_platinum'])
            warframe_price_df.loc[warframe, item] = item_price['ingame_lowest_sell_platinum']

    progress.empty()

    return warframe_price_df

@st.cache(show_spinner=False, suppress_st_warning=True, ttl=86400.0)
def get_weapon_price():

    weapon_prime_list = ['burston','tenora','vectis','braton']
    weapon_prime_set_list = ['set', 'blueprint', 'receiver', 'stock', 'barrel']

    weapon_price_df = pd.DataFrame(data=np.zeros((len(weapon_prime_list),len(weapon_prime_set_list)), dtype = int), index=weapon_prime_list, columns=weapon_prime_set_list)
    weapon_price_df.insert(column='item_name', value='')

    progress = st.empty()

    for i, weapon in enumerate(weapon_prime_list):
        progress.write(f"🚴‍♂️ **{weapon.upper()}** ...")
        for item in weapon_prime_set_list:
            url_name = weapon + '_prime_' + item
            # if warframe=='khora':
            #     if item in ['neuroptics', 'chassis', 'systems']:
            #         url_name = url_name + '_blueprint'
            item_orders = get_item_orders(url_name)
            item_price = get_item_price(item_orders['orders'])
            item_info = get_item_info(url_name)


            # ducats = int(info['info'].get('ducats', '--'))
            # label = "💛" if ducats==100 else ""    
            # warframe_price_df.loc[warframe, item] = str(item_price['ingame_lowest_sell_platinum']) + ' - ' + str(item_price['ingame_highest_buy_platinum'])
            weapon_price_df.loc[weapon, item] = item_price['ingame_lowest_sell_platinum']

    progress.empty()

    return weapon_price_df