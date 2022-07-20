import streamlit as st
from scripts.wmmarket import item_orders
from scripts.core import item_price

warframe_prime_list = ['ash', 'atlas', 'banshee', 'chroma', 'ember', 'equinox', 'frost', 'gara', 'garuda', 'harrow', 'hydroid', 'inaros', 'ivara', 'khora', 'limbo', 'loki', 'mag',
                           'mesa', 'mirage', 'nekros', 'nezha', 'nidus', 'nova', 'nyx', 'oberon', 'octavia', 'rhino', 'saryn', 'titania', 'trinity', 'valkyr', 'vauban', 'volt', 'wukong', 'zephyr']
warframe_prime_set_list = ['set', 'blueprint', 'neuroptics', 'chassis', 'systems']


for warframe in warframe_prime_list:
    cols = st.columns(len(warframe_prime_set_list))
    for i, item in enumerate(warframe_prime_set_list):
        with cols[i]:
            item_name = warframe + '_prime_' + item
            st.write(i, item_name)
