from requests import URLRequired
import streamlit as st
from scripts.wmmarket import item_orders
from scripts.core import item_price
import time

warframe_prime_list = ['ash', 'atlas', 'banshee', 'chroma', 'ember', 'equinox', 'frost', 'gara', 'garuda', 'harrow', 'hydroid', 'inaros', 'ivara', 'khora', 'limbo', 'loki', 'mag',
                           'mesa', 'mirage', 'nekros', 'nezha', 'nidus', 'nova', 'nyx', 'oberon', 'octavia', 'rhino', 'saryn', 'titania', 'trinity', 'valkyr', 'vauban', 'volt', 'wukong', 'zephyr']
warframe_prime_set_list = ['set', 'blueprint', 'neuroptics', 'chassis', 'systems']

cols = st.columns(len(warframe_prime_set_list)+1)
col_name = ['名称','套装','蓝图','头部','机体','系统']
for i, name in enumerate(col_name):
    with cols[i]:
        st.write(name)

for warframe in warframe_prime_list:
    with cols[0]:
        st.write(f"**{warframe}**")
    for i, item in enumerate(warframe_prime_set_list):
        with cols[i+1]:
            url_name = warframe + '_prime_' + item
            if warframe=='khora':
                if item in ['neuroptics', 'chassis', 'systems']:
                    url_name = url_name + '_blueprint'
            orders = item_orders(url_name)
            price = item_price(orders['orders'])
            st.write(f"**{price['ingame_lowest_sell_platinum']}**")
