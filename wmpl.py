

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
  }
  requests_result = requests.get(f'https://api.warframe.market/v1/items/{item_name}/orders', headers={'Platform': 'pc'})
  st.write(requests_result)
  # payload = json.loads(result.text)
  # orders = payload['payload']['orders']
  # high_buy_price = 0
  # buy_user = ''
  # low_sell_price = 0
  # sell_user = ''
  # for order in orders:
  #   if order['order_type']=='sell' and order['user']['status']=='ingame':
  #     # print('sell', order['platinum'], order['user']['ingame_name'])
  #     if low_sell_price==0:
  #       low_sell_price = order['platinum']
  #       sell_user = order['user']['ingame_name']
  #     else:
  #       if order['platinum']<low_sell_price:
  #         low_sell_price = order['platinum']
  #         sell_user = order['user']['ingame_name']
  #   if order['order_type']=='buy' and order['user']['status']=='ingame':
  #     # print('buy', order['platinum'], order['user']['ingame_name'])
  #     if high_buy_price==0:
  #       high_buy_price = order['platinum']
  #       buy_user = order['user']['ingame_name']
  #     else:
  #       if order['platinum']>high_buy_price:
  #         high_buy_price = order['platinum']
  #         buy_user = order['user']['ingame_name']
  # end_time = time.time()
  # last_time = end_time-start_time
  # time_text = 'time: '+ str(round(last_time, 3))
  # st.text(time_text)
  # st.text(name)
  # low_price = '低卖：' + str(low_sell_price) + ' ' + sell_user
  # st.text(low_price)
  # high_price = '高买：' + str(high_buy_price) + ' ' + buy_user
  # st.text(high_price)
  return order_info

st.title('Warframe Market Price List')

warframe_prime_list = ['ash', 'atlas', 'banshee']
warframe_prime_set_list = ['set', 'blueprint', 'neuroptics', 'chassis', 'systems']

st.write(get_order_info('ash_prime_set'))
