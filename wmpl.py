

import streamlit as st
import pandas as pd
import requests
import json
import time

def get_order_info(item_name):  
  start_time = time.time()
  order_info = {
    'name': item_name,
    'sell': 0,
    'seller': '',
    'buy': 0,
    'buyer': '', 
    'time': 0,
    'status': '',
  }
  requests_result = requests.get(f'https://api.warframe.market/v1/items/{item_name}/orders', headers={'Platform': 'pc'})
  
  if order_info['status'] == '<Response [200]>':
      order_info['status'] = 'T'
      payload = json.loads(requests_result.text)
      orders = payload['payload']['orders']
      for order in orders:
        if order['user']['status']=='ingame':
          if order['order_type']=='sell':
            if order_info['sell']==0:
              order_info['sell'] = order['platinum']
              order_info['seller'] = order['user']['ingame_name']
            else:
              if order['platinum']<order_info['sell']:
                order_info['sell'] = order['platinum']
                order_info['seller'] = order['user']['ingame_name']
          if order['order_type']=='buy':
            if order_info['buy']==0:
              order_info['buy'] = order['platinum']
              order_info['buyer'] = order['user']['ingame_name']
            else:
              if order['platinum']>order_info['buy']:
                order_info['buy'] = order['platinum']
                order_info['buyer'] = order['user']['ingame_name']
      order_info['time'] = str(round(time.time()-start_time,3))
   else:
      order_info['status'] = 'F'
  return order_info

st.title('Warframe Market Price List')

warframe_prime_list = ['ash', 'atlas', 'banshee']
warframe_prime_set_list = ['set', 'blueprint', 'neuroptics', 'chassis', 'systems']

price_df = pd.DataFrame(columns = ['name', 'sell', 'seller', 'buy', 'buyer', 'time', 'status'])
for warframe in warframe_prime_list:
  item_name = warframe+'_prime_set'
  price_df.loc[len(price_df)] = get_order_info(item_name)
  
st.dataframe(price_df)
