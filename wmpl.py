

import streamlit as st
import pandas as pd
import requests
import json
import time

st.title('Warframe Market Price List - Streamlit')

start_time = time.time()
name = 'ash_prime_set'
result = requests.get(f'https://api.warframe.market/v1/items/{name}/orders', headers={'Platform': 'pc'})
st.text(result)
payload = json.loads(result.text)
orders = payload['payload']['orders']
high_buy_price = 0
buy_user = ''
low_sell_price = 0
sell_user = ''
for order in orders:
  if order['order_type']=='sell' and order['user']['status']=='ingame':
    # print('sell', order['platinum'], order['user']['ingame_name'])
    if low_sell_price==0:
      low_sell_price = order['platinum']
      sell_user = order['user']['ingame_name']
    else:
      if order['platinum']<low_sell_price:
        low_sell_price = order['platinum']
        sell_user = order['user']['ingame_name']
  if order['order_type']=='buy' and order['user']['status']=='ingame':
    # print('buy', order['platinum'], order['user']['ingame_name'])
    if high_buy_price==0:
      high_buy_price = order['platinum']
      buy_user = order['user']['ingame_name']
    else:
      if order['platinum']>high_buy_price:
        high_buy_price = order['platinum']
        buy_user = order['user']['ingame_name']
end_time = time.time()
last_time = end_time-start_time
time_text = 'time: '+ str(round(last_time, 3))
st.text(time_text)
st.text(name)
low_price = '低卖：' + str(low_sell_price) + ' ' + sell_user
st.text(low_price)
high_price = '高买：' + str(high_buy_price) + ' ' + buy_user
st.text(high_price)
