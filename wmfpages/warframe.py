import streamlit as st
from wmfpkg.wmmarket import get_items
from wmfpkg.wmfcore import show_item


def page():
    warframe_prime_list = ['ash', 'atlas', 'banshee', 'chroma', 'ember', 'equinox', 'frost', 'gara', 'garuda', 'harrow', 'hydroid', 'inaros', 'ivara', 'limbo', 'loki', 'mag',
                           'mesa', 'mirage', 'nekros', 'nezha', 'nidus', 'nova', 'nyx', 'oberon', 'octavia', 'rhino', 'saryn', 'titania', 'trinity', 'valkyr', 'vauban', 'volt', 'wukong', 'zephyr']
    warframe_prime_set_list = ['set', 'blueprint',
                               'neuroptics', 'chassis', 'systems']
    warframe_selection = st.selectbox('选择战甲', warframe_prime_list)
    items = items()
    for item in warframe_prime_set_list:
        item_name = warframe_selection + '_prime_' + item
        item_df = items[items['url_name'] == item_name]
        show_item(item_df)
    return
