import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

st.set_page_config(page_title='Warframe Farmer', page_icon='random', layout="wide", initial_sidebar_state="expanded", menu_items=None)

# mode_list = ["虚空裂缝", '警报 - 噩梦']
# containers = {}
# for item in mode_list:
#     containers[item] = st.empty()
# toc_selectbox = st.sidebar.selectbox("任务选择：", mode_list)

# tag = 'tag'
# with containers[toc_selectbox].container():
#     if tag != toc_selectbox:
#         if containers.get(tag):
#             containers[tag] = st.empty()
#         tag = toc_selectbox
#     st.write(toc_selectbox)
#     st.write(tag)
        
    
@st.cache
def get_droptables():
  droptables = {}
  r = requests.get('https://www.warframe.com/droptables')
  if r.status_code == 200:
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
    
    # Relics
    id = toc_dict['Relics']
    relic_dict = {}
    relics = soup.find('h3', id=id)
    relics_table = relics.next_sibling.next_sibling    
    relic_count = int(len(relics_table.find_all('tr'))/8/4)
    relic_tag = relics_table.tr

    for i in range(relic_count+1):
        relic_drops = {}
        relic_name = relic_tag.text.split(' (')[0].lower()
        
        for n in range(6):
            relic_tag = relic_tag.next_sibling
            relic_drops[relic_tag.td.text.lower()] = int(relic_tag.td.next_sibling.text.split('.')[0].split('(')[1])
        relic_drops = sorted(relic_drops.items(), key=lambda x: x[1], reverse=True)
        relic_dict[relic_name] = [x[0] for x in relic_drops]

        for n in range(34):
            if relic_tag.next_sibling:
                relic_tag = relic_tag.next_sibling
     
    # Nightmare
    nightmare_dict = {}

    droptables['relics'] = relic_dict
    droptables['nightmare'] = nightmare_dict
    
  return droptables

@st.cache
def get_url_names():
  url_names = {}
  r = requests.get('https://api.warframe.market/v1/items', headers={'Language': 'zh-hans'})
  if r.status_code == 200:
      payload = r.json()
      items = payload['payload']['items']
      for item in items:
          url_names[item['url_name']] = item['item_name']
  return url_names

@st.cache(show_spinner=False, ttl=120.0)
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
  
  r = requests.get(f'https://api.warframe.market/v1/items/{item_name}/orders', headers={'Platform': 'pc'})
  
  if r.status_code == 200:
      order_info['status'] = 'T'
      payload = r.json()
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
  
droptables = get_droptables()
url_names = get_url_names()


relic_drop_col = [0,1,2,3]
relic_type_col, relic_drop_col[0],relic_drop_col[1],relic_drop_col[2],relic_drop_col[3]  = st.columns([1,2,2,2,2])

with relic_type_col:
  relic_type = st.radio('纪元', ('古纪', '前纪', '中纪', '后纪', '安魂'))

relic_prefix = {
    '古纪': 'lith',
    '前纪': 'meso',
    '中纪': 'neo',
    '后纪': 'axi',
    '安魂': 'requiem',
}
warframe_prime_list = ['ash', 'atlas', 'banshee', 'chroma', 'ember', 'equinox', 'frost', 'gara', 'harrow', 'hydroid', 'inaros', 'ivara', 'limbo', 'loki', 'mag', 'mesa', 'mirage', 'nekros', 'nezha', 'nidus', 'nova', 'nyx', 'oberon', 'octavia', 'rhino', 'saryn', 'titania', 'trinity', 'valkyr', 'vauban', 'volt', 'wukong', 'zephyr']

def show_price(item_name):
# with relic_drop_col[0]:
#     item_name = st.text_input('').lower()
    item_name = relic_prefix[relic_type]+ ' ' + item_name + ' relic'
    drop_list = droptables['relics'].get(item_name)
    if drop_list:
      df = pd.DataFrame()
      df['url_name'] = drop_list 
      drop_list_cn = []
      price_list = []
      for item in drop_list:
        if 'neuroptics' in item or 'chassis' in item or 'systems' in item:
          if item.split(' ')[0] in warframe_prime_list:
            item = item[:-10]
        url_name = item.replace(' ','_')
        cn_name = url_names.get(url_name.lower())
        if url_name == 'forma_blueprint':
          cn_name = 'Forma 蓝图'
        drop_list_cn.append(cn_name)
        price = get_order_info(url_name.lower())['buy']
        price_list.append(price)
      df['中文'] = drop_list_cn
      df['价格'] = price_list
      st.table(df[['中文','价格']])

itemname = st.text_input('').lower()

names = itemname.strip().split(' ')

for x, y in enumerate(names):
  st.write(x, y)
  with relic_drop_col[x]:
    show_price(y)

nightmaremoderewards = ['Ice Storm','Stunning Speed','Hammer Shot','Wildfire','Accelerated Blast','Blaze','Chilling Reload','Drifting Contact','Seeking Fury','Armored Agility','Shred','Rending Strike','Fortitude','Streamlined Form','Animal Instinct','Vigor','Lethal Torrent','Focus Energy','Constitution']

night = pd.DataFrame()
night['url_name'] = nightmaremoderewards.replace(' ','_').lower()
st.table(night)

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
