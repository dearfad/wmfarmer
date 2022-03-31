import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title='Warframe Market Farmer', page_icon='random')

items_api_url = "https://api.warframe.market/v1/items"
assets_url = "https://warframe.market/static/assets/"

@st.cache
def get_items(suppress_st_warning=True):
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

@st.cache(show_spinner=False, ttl=120.0)
def get_order_info(item_name):  
  order_info = {
    'name': item_name,
    'sell': 0,
    'seller': '',
    'buy': 0,
    'buyer': '', 
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
  else:
      order_info['status'] = 'F'
  return order_info


st.title('Warframe Market Farmer')
item_name = st.text_input('名称：', 'Xiphos 机身')
items = get_items()
item = items[items['item_name_cn']==item_name].to_dict(orient='records')
if item:
  thumb_url = assets_url + item['thumb']
  order_info = get_order_info(item['url_name'])
  col0, col1, col2 = st.columns(3)
  col0.image(thumb_url)
  col1.metric("最高卖出", order_info['buy'], order_info['buyer'])
  col2.metric("最低买入", order_info['sell'], order_info['seller'])
else:
  st.write('未找到相关信息...')
