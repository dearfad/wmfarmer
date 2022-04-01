 
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
  with relic_drop_col[x]:
    show_price(y)

