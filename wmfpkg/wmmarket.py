import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timezone, timedelta

items_api_url = "https://api.warframe.market/v1/items"


@st.cache(show_spinner=False, suppress_st_warning=True)
def get_items():
    r_en = requests.get(items_api_url, headers={"Language": "en"})
    if r_en.status_code == 200:
        items_en = pd.json_normalize(r_en.json()["payload"]["items"])
        items_en.rename(columns={"item_name": "item_name_en"}, inplace=True)
    r_cn = requests.get(items_api_url, headers={"Language": "zh-hans"})
    if r_cn.status_code == 200:
        items_cn = pd.json_normalize(r_cn.json()["payload"]["items"])
        items_cn.rename(columns={"item_name": "item_name_cn"}, inplace=True)
    items = pd.merge(items_cn, items_en)
    # items[items.item_name_cn.duplicated(keep=False)]
    return items


@st.cache(show_spinner=False, suppress_st_warning=True, ttl=120.0)
def get_order_info(url_name):
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

if __name__ == '__main__':
    items = get_items()
    print(items.columns)
    order_info = get_order_info('xiphos_fuselage')
    print(order_info)
    