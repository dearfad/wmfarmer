# Warframe.market API
# https://warframe.market/zh-hans/api_docs
# Author: dearfad
# Email: dearfad@sina.com

import pandas as pd
import requests
import streamlit as st

apiVersion = 'v1'
Servers = "https://api.warframe.market/"
Computed_URL = Servers + apiVersion

# ===============================================================
# Items: Provides all information about common items data models.
# ===============================================================

items_api_url = Computed_URL + "/items"


# @st.cache(show_spinner=False, suppress_st_warning=True, ttl=86400.0)
def get_items(language='zh-hans'):
    # items: Get list of all tradable items.
    # ['id', 'thumb', 'url_name', 'item_name_cn', 'item_name_en']
    # Language : en, ru, ko, de, fr, pt, zh-hans, zh-hant, es, it, pl

    headers = {'Language': language, 'Connection': 'close', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
    r = requests.get(items_api_url, headers=headers)
    st.write(r.headers)
    items = pd.DataFrame()
    if r.status_code == 200:
        items = pd.DataFrame(r.json()['payload']['items'])
        st.write('get_items OK!')
    else:
        st.write(f"get_items {r.status_code}")

    return items


# @st.cache(show_spinner=False, suppress_st_warning=True, ttl=86400.0)
def get_item_info(url_name):
    # items_info: Gets information about an item
    headers = {"Platform": "pc", 'Connection': 'close', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
    r = requests.get(f'{items_api_url}/{url_name}', headers=headers)
    st.write(r.headers)
    item_info = {}
    if r.status_code == 200:
        item_json = r.json()['payload']['item']
        for item in item_json['items_in_set']:
            if item['url_name'] == url_name:
                item_info = item
    else:
        st.write(f"get_item_info {r.status_code}")

    return item_info


@st.cache(show_spinner=False, suppress_st_warning=True, ttl=60.0)
def get_item_orders(url_name):
    # item_orders: Get list of orders for a given item_id
    # st.cache
    # ttl = 60.0 Change if Needed
    # The maximum number of seconds to keep an entry in the cache,
    # or None if cache entries should not expire. The default is None.

    headers = {"Platform": "pc", 'Connection': 'close', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
    r = requests.get(f'{items_api_url}/{url_name}/orders',
                     headers=headers)  
    item_orders = ''
    if r.status_code == 200:
        item_orders = r.json()['payload']['orders']
    else:
        st.write(f"get_item_orders {r.status_code}")
    return item_orders


@st.cache(show_spinner=False, suppress_st_warning=True)
def items_droptables(url_name):
    # items_droptables: Get droptables for a given item
    pass


if __name__ == '__main__':

    # test items()
    # items = get_items()
    # print(items.head(1))

    # test items_info()
    # item_info = get_item_info('mirage_prime_systems')
    # item_info = get_item_info('hammer_shot')
    # print(item_info)
    # print(item_info.keys())
    # print(item_info['zh-hans'])

    # test item_orders
    # orders = get_item_orders('hammer_shot')
    # print(orders)

    pass