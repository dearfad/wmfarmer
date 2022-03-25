import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_droptables():
  droptables = {}
  r = requests.get('https://www.warframe.com/droptables')
  if r.status_code==200:
    soup = BeautifulSoup(r.text)
    toc = soup.ul
    dynamic_location_rewards =soup.ul.ul

    toc_dict = {}
    for item in toc:
        if item.name:
            toc_dict[item.a.text] = item.a['href'].strip('#')

    dynamic_location_rewards_dict = {}
    for item in dynamic_location_rewards:
        if item.name:
            dynamic_location_rewards_dict[item.a.text] = item.a['href'].strip('#')
    
    id = toc_dict['Relics']

    relics = soup.find('h3', id=id)

    relics_table = relics.next_sibling.next_sibling

    relic_dict = {}

    relic_count = int(len(relics_table.find_all('tr'))/8/4)

    relic_tag = relics_table.tr

    for i in range(relic_count+1):
        relic_name = relic_tag.text.split(' (')[0]
        relic_drops = []
        for n in range(6):
            relic_tag = relic_tag.next_sibling
            relic_drops.append(relic_tag.td.text)
        relic_dict[relic_name] = relic_drops

        for n in range(34):
            if relic_tag.next_sibling:
                relic_tag = relic_tag.next_sibling
    
    droptables['Relics'] = relic_dict
    
  return droptables

def get_url_names():
  url_names = {}
  r = requests.get('https://api.warframe.market/v1/items', headers={'Language': 'zh-hans'})
  if r.statuscode == 200:
      payload = result.json()
      items = payload['payload']['items']
      for item in items:
          url_names[item['url_name']] = item['item_name']]
  return url_names

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
  
  if str(requests_result) == '<Response [200]>':
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

st.title('Warframe Farmer')

with st.empty():
  st.info('从Warframe官网获取掉落表...')
  droptables = get_droptables()
  st.info('从Market官网获取中文对照表...')
  url_names = get_url_names()
  st.write('')

st.write(url_names)

# warframe_prime_list = ['ash', 'atlas', 'banshee', 'chroma', 'ember', 'equinox', 'frost', 'gara', 'harrow', 'hydroid', 'inaros', 'ivara', 'limbo', 'loki', 'mag', 'mesa', 'mirage', 'nekros', 'nezha', 'nidus', 'nova', 'nyx', 'oberon', 'octavia', 'rhino', 'saryn', 'titania', 'trinity', 'valkyr', 'vauban', 'volt', 'wukong', 'zephyr']
# warframe_prime_set_list = ['set', 'blueprint', 'neuroptics', 'chassis', 'systems']



# price_df = pd.DataFrame(columns = ['name', 'sell', 'seller', 'buy', 'buyer', 'time', 'status'])

# warframe_selection = st.sidebar.selectbox('选择战甲', warframe_prime_list)

# with st.empty():
#   for item in warframe_prime_set_list:
#     item_name = warframe_selection + '_prime_' + item
#     st.info(item_name)
#     price_df.loc[len(price_df)] = get_order_info(item_name)
#   st.write('')

# # for warframe in warframe_prime_list:
# #   for item in warframe_prime_set_list:
# #     item_name = warframe + '_prime_' + item
# #     price_df.loc[len(price_df)] = get_order_info(item_name)
  
# st.dataframe(price_df, height=800)
