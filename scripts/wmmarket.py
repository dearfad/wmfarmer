# Warframe.market API
# https://warframe.market/zh-hans/api_docs
# Author: dearfad
# Email: dearfad@sina.com

import pandas as pd
import requests
import streamlit as st
from datetime import datetime, timedelta, timezone

apiVersion = 'v1'
Servers = "https://api.warframe.market/"
Computed_URL = Servers + apiVersion


def get_time():
    utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    time = utc_time.astimezone(
        timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    return time

# ===============================================================
# Items: Provides all information about common items data models.
# ===============================================================

items_api_url = Computed_URL + "/items"


@st.cache(show_spinner=True, suppress_st_warning=False, ttl=86400.0)
def items(language='zh-hans'):
    # items: Get list of all tradable items.
    # ['id', 'thumb', 'url_name', 'item_name_cn', 'item_name_en']
    # Language : en, ru, ko, de, fr, pt, zh-hans, zh-hant, es, it, pl

    headers = {'Language': language}
    r = requests.get(items_api_url, headers=headers)

    items = {}
    if r.status_code == 200:
        items['time'] = get_time()
        items['items'] = pd.DataFrame(r.json()['payload']['items'])
    else:
        items['time'] = 'failed'
        items['items'] = r.status_code
    return items


@st.cache(show_spinner=False, suppress_st_warning=True, ttl=86400.0)
def item_info(url_name):
    # items_info: Gets information about an item
    headers = {"Platform": "pc"}
    r = requests.get(f'{items_api_url}/{url_name}', headers=headers)
    item_info = {}
    if r.status_code == 200:
        item_json = r.json()['payload']['item']
        for item in item_json['items_in_set']:
            if item['url_name'] == url_name:
                item_info['info'] = item
                item_info['time'] = get_time()

    else:
        st.write(f"get_item_info {r.status_code}")
    return item_info


@st.cache(show_spinner=False, suppress_st_warning=True, ttl=1.0)
def item_orders(url_name):
    # item_orders: Get list of orders for a given item_id
    # st.cache
    # ttl = 60.0 Change if Needed
    # The maximum number of seconds to keep an entry in the cache,
    # or None if cache entries should not expire. The default is None.

    headers = {"Platform": "pc"}
    r = requests.get(f'{items_api_url}/{url_name}/orders',
                     headers=headers)  
    item_orders = {}
    if r.status_code == 200:
        item_orders['orders'] = r.json()['payload']['orders']
        item_orders['time'] = get_time()
    else:
        st.write(f"get_item_orders {r.status_code}")
    return item_orders


@st.cache(show_spinner=False, suppress_st_warning=True)
def items_droptables(url_name):
    # items_droptables: Get droptables for a given item
    pass

