import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title='Warframe Market Farmer', page_icon='random')

items_api_url = "https://api.warframe.market/v1/items"
assets_url = "https://warframe.market/static/assets/"

@st.cache(suppress_st_warning=True)
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

@st.cache(suppress_st_warning=True, show_spinner=False, ttl=120.0)
def get_order_info(item_name):  
  order_info = {'name': item_name, 'sell': 0, 'seller': '', 'buy': 0, 'buyer': '',  'status': ''} 
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

@st.cache(suppress_st_warning=True)
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
#     dynamic_location_rewards_dict = {}
#     for item in dynamic_location_rewards:
#         if item.name:
#             dynamic_location_rewards_dict[item.a.text] = item.a['href'].strip('#')    
    # Relics
    id = toc_dict['Relics']
    relic_dict = {}
    relics = soup.find('h3', id=id)
    relics_table = relics.next_sibling.next_sibling    
    relic_count = int(len(relics_table.find_all('tr'))/8/4)
    relic_tag = relics_table.tr
    for i in range(relic_count+1):
        relic_drops = {}
        relic_name = relic_tag.text.split(' (')[0]   
        for n in range(6):
            relic_tag = relic_tag.next_sibling
            relic_drops[relic_tag.td.text] = int(relic_tag.td.next_sibling.text.split('.')[0].split('(')[1])
        relic_drops = sorted(relic_drops.items(), key=lambda x: x[1], reverse=True)
        relic_dict[relic_name] = [x[0] for x in relic_drops]
        for n in range(34):
            if relic_tag.next_sibling:
                relic_tag = relic_tag.next_sibling  
    droptables['relics'] = relic_dict
    # Nightmare
    # nightmare_dict = {}
    # droptables['nightmare'] = nightmare_dict    
  return droptables

def show_item(item_df):
  item = item_df.to_dict(orient='records')[0]
  thumb_url = assets_url + item['thumb']
  order_info = get_order_info(item['url_name'])
  st.markdown('**'+item['item_name_cn']+'**')
  col0, col1, col2 = st.columns(3)
  col0.image(thumb_url)
  col1.metric("最高卖出", order_info['buy'], order_info['buyer'])
  col2.metric("最低买入", order_info['sell'], order_info['seller'])
  return

def item():
  item_name = st.text_input('模糊搜索：', 'Xiphos 机身')
  items = get_items()
  search_result = items[items['item_name_cn'].str.contains(item_name.capitalize())]
  item_names = search_result['item_name_cn'].values
  selected_name = st.selectbox('已发现：', item_names)
  item_df = items[items['item_name_cn']==selected_name]
  if item_df.empty:
    st.write(selected_name, '未找到相关信息...')  
  else:
    show_item(item_df)
  return

def nightmare():
  nightmaremoderewards = ['Ice Storm','Stunning Speed','Hammer Shot','Wildfire','Accelerated Blast','Blaze','Chilling Reload','Drifting Contact','Seeking Fury','Armored Agility','Shred','Rending Strike','Fortitude','Streamlined Form','Animal Instinct','Vigor','Lethal Torrent','Focus Energy','Constitution']
  items = get_items()
  for item_name in nightmaremoderewards:
    item_df = items[items['item_name_en']==item_name]
    show_item(item_df)
    # r_a = '水星 金星 地球 火星'
    # r_b = '火卫一 谷神星 木星 欧罗巴 土星 月球 虚空 赤毒要塞 火卫二'
    # r_c = '天王星 海王星 冥王星 阋神星 赛德娜'
    # night['位置'] = [r_a,r_a,r_a,r_a,r_a,r_a,r_a,r_b,r_b,r_b,r_b,r_b,r_b,r_c,r_c,r_c,r_c,r_c,r_c,]
    # st.table(night)
  return

def warframe():
  warframe_prime_list = ['ash', 'atlas', 'banshee', 'chroma', 'ember', 'equinox', 'frost', 'gara', 'garuda', 'harrow', 'hydroid', 'inaros', 'ivara', 'limbo', 'loki', 'mag', 'mesa', 'mirage', 'nekros', 'nezha', 'nidus', 'nova', 'nyx', 'oberon', 'octavia', 'rhino', 'saryn', 'titania', 'trinity', 'valkyr', 'vauban', 'volt', 'wukong', 'zephyr']
  warframe_prime_set_list = ['set', 'blueprint', 'neuroptics', 'chassis', 'systems']
  warframe_selection = st.selectbox('选择战甲', warframe_prime_list)
  items = get_items()
  for item in warframe_prime_set_list:
    item_name = warframe_selection + '_prime_' + item
    item_df = items[items['url_name']==item_name]
    show_item(item_df)
  return

def relic():
  items = get_items()
  droptables = get_droptables()
  
  item_name = st.text_input('模糊搜索：', 'A1') 
  search_result = []
  for key in droptables['relics']:
    if item_name.capitalize() in key:
      search_result.append(key)
  item_name_cn = []
  for item in search_result:
    item_name_cn.append(items[items['item_name_en']==item]['item_name_cn'].values[0])
  selected_name = st.selectbox('已发现：', item_name_cn)
  selected_relic_name_en = items[items['item_name_cn']==selected_name]['item_name_en'].values[0]
  relic_drop = droptables['relics'][selected_relic_name_en]
  for item in relic_drop:
    if 'Chassis Blueprint' in item or 'Systems Blueprint' in item or 'Neuroptics Blueprint' in item:
      item = item[:-10]
    item_df = items[items['item_name_en']==item]
    if item_df.empty:
      if item == 'Forma Blueprint':
        st.markdown('**福马 蓝图**')
        col0, col1, col2 = st.columns(3)
        col0.image('https://static.wikia.nocookie.net/warframe/images/b/b1/Forma2.png', width=128)
        col1.metric("最高卖出", 0)
        col2.metric("最低买入", 0)
      else:
        st.write(item, '未找到相关信息...')  
    else:
      show_item(item_df)
  return

def main():
  pages = {
    '物品价格': item,
    '战甲套装': warframe,
    '噩梦收益': nightmare,
    '虚空裂缝': relic
  }
  with st.sidebar:
    st.title('Warframe Market Farmer')
    page = st.radio("请选择：", pages.keys())

  pages[page]()
  
if __name__=='__main__':
    
    # Baidu Stat
    baidu_stat = '''
    <script>
    var _hmt = _hmt || [];
    (function() {
      var hm = document.createElement("script");
      hm.src = "https://hm.baidu.com/hm.js?b8d6c662233ffe44f986f97f4553a0d1";
      var s = document.getElementsByTagName("script")[0]; 
    '''
    components.html(baidu_stat)
    main()
