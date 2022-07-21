import streamlit as st
from scripts.wmmarket import item_orders, item_info
from scripts.core import item_price
import pandas as pd
import numpy as np

warframe_prime_list = ['ash', 'atlas', 'banshee', 'chroma', 'ember', 'equinox', 'frost', 'gara', 'garuda', 'harrow', 'hydroid', 'inaros', 'ivara', 'khora', 'limbo', 'loki', 'mag',
                           'mesa', 'mirage', 'nekros', 'nezha', 'nidus', 'nova', 'nyx', 'oberon', 'octavia', 'rhino', 'saryn', 'titania', 'trinity', 'valkyr', 'vauban', 'volt', 'wukong', 'zephyr']
warframe_prime_set_list = ['set', 'blueprint', 'neuroptics', 'chassis', 'systems']


warframe_df = pd.DataFrame(data=np.zeros((len(warframe_prime_list),len(warframe_prime_set_list)), dtype = int), index=warframe_prime_list, columns=warframe_prime_set_list)


for warframe in warframe_prime_list:
    for item in enumerate(warframe_prime_set_list):
        url_name = warframe + '_prime_' + item
        if warframe=='khora':
            if item in ['neuroptics', 'chassis', 'systems']:
                url_name = url_name + '_blueprint'
        orders = item_orders(url_name)
        price = item_price(orders['orders'])
        info = item_info(url_name)

        warframe_df.loc[warframe, item] = price['ingame_lowest_sell_platinum']

        # st.write(f"**{price['ingame_lowest_sell_platinum']}**")
        # ducats = int(info['info'].get('ducats', '--'))
        # label = "💛" if ducats==100 else ""
        # st.write(f"**{price['ingame_highest_buy_platinum']}** {label}")

st.write(warframe_df)