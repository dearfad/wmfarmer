

import streamlit as st
import pandas as pd
import requests
import json
import time

def get_order_info(item_name):  
  start_time = time.time()
  order_info = {
    'item_name': item_name,
    'lowest_sell_price': 0,
    'sell_user': '',
    'highest_buy_price': 0,
    'buy_user': '', 
    'query_time': 0,
    'status': '',
  }
  requests_result = requests.get(f'https://api.warframe.market/v1/items/{item_name}/orders', headers={'Platform': 'pc'})
  order_info['status'] = requests_result
  if order_info['status'] == '<Response [200]>':
    print('ok')
    payload = json.loads(request_result.text)
    orders = payload['payload']['orders']
    for order in orders:
      if order['user']['status']=='ingame':
        if order['order_type']=='sell':
          if order_info['lowest_sell_price']==0:
            order_info['lowest_sell_price'] = order['platinum']
            order_info['sell_user'] = order['user']['ingame_name']
          else:
            if order['platinum']<order_info['lowest_sell_price']:
              order_info['lowest_sell_price'] = order['platinum']
              order_info['sell_user'] = order['user']['ingame_name']
        if order['order_type']=='buy':
          if order_info['highest_buy_price']==0:
            order_info['highest_buy_price'] = order['platinum']
            order_info['buy_user'] = order['user']['ingame_name']
          else:
            if order['platinum']>order_info['highest_buy_price']:
              order_info['highest_buy_price'] = order['platinum']
              order_info['buy_user'] = order['user']['ingame_name']
    order_info['query_time'] = str(round(time.time()-start_time,3))
  return order_info

st.title('Warframe Market Price List')

warframe_prime_list = ['ash', 'atlas', 'banshee']
warframe_prime_set_list = ['set', 'blueprint', 'neuroptics', 'chassis', 'systems']

st.write(get_order_info('ash_prime_set'))
