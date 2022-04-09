# Warframe.market API
# https://warframe.market/zh-hans/api_docs
# Author: dearfad
# Email: dearfad@sina.com


from datetime import datetime, timedelta, timezone

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


@st.cache(show_spinner=False, suppress_st_warning=True)
def get_items():
    # items: Get list of all tradable items.
    # combine item_name en and zh-hans
    # ['id', 'thumb', 'url_name', 'item_name_cn', 'item_name_en']

    # en for droptables
    r_en = requests.get(items_api_url, headers={"Language": "en"})
    if r_en.status_code == 200:
        items_en = pd.json_normalize(r_en.json()["payload"]["items"])
        items_en.rename(columns={"item_name": "item_name_en"}, inplace=True)
        
    # zh-hans 
    r_cn = requests.get(items_api_url, headers={"Language": "zh-hans"})
    if r_cn.status_code == 200:
        items_cn = pd.json_normalize(r_cn.json()["payload"]["items"])
        items_cn.rename(columns={"item_name": "item_name_cn"}, inplace=True)

    items_df = pd.merge(items_cn, items_en)

    # duplicated items EXIST, change if needed
    # items[items.item_name_cn.duplicated(keep=False)]
    return items_df


@st.cache(show_spinner=False, suppress_st_warning=True)
def get_item_info(url_name):
    # items_info: Gets information about an item
    r = requests.get(f'{items_api_url}/{url_name}', headers={"Platform": "pc"})
    if r.status_code == 200:
        item_info = {}
        item_json = r.json()['payload']['item']
        for item in item_json['items_in_set']:
            if item['url_name'] == url_name:
                item_info = item
    return item_info


@st.cache(show_spinner=False, suppress_st_warning=True, ttl=60.0)
def items_orders(url_name):
    # item_orders: Get list of orders for a given item_id
    # st.cache
    # ttl = 60.0 Change if Needed
    # The maximum number of seconds to keep an entry in the cache,
    # or None if cache entries should not expire. The default is None.
    order_info = {'name': url_name, 'sell': 0, 'seller': '',
                  'buy': 0, 'buyer': '',  'status': '', 'time': ''}
    r = requests.get(f'{items_api_url}/{url_name}/orders',
                     headers={'Platform': 'pc'})
    if r.status_code == 200:
        order_info['status'] = 'T'
        utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)
        order_info['time'] = utc_time.astimezone(
            timezone(timedelta(hours=8))).strftime("%H:%M:%S")
        orders = r.json()['payload']['orders']
        for order in orders:
            if order['user']['status'] == 'ingame':
                if order['order_type'] == 'sell':
                    if order_info['sell'] == 0 or order['platinum'] < order_info['sell']:
                        order_info['sell'] = order['platinum']
                        order_info['seller'] = order['user']['ingame_name']
                if order['order_type'] == 'buy':
                    if order_info['buy'] == 0 or order['platinum'] > order_info['buy']:
                        order_info['buy'] = order['platinum']
                        order_info['buyer'] = order['user']['ingame_name']
    else:
        order_info['status'] = 'F'
    return order_info


@st.cache(show_spinner=False, suppress_st_warning=True)
def items_droptables(url_name):
    # items_droptables: Get droptables for a given item
    pass


if __name__ == '__main__':

    # test items()
    # items = items()
    # print(items.head(1))

    # test items_info()
    item_info = get_item_info('mirage_prime_systems')
    # item_info = get_item_info('hammer_shot')
    # print(item_info)
    print(item_info.keys())
    print(item_info['zh-hans'])

