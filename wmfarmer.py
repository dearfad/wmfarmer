from pandas.core import series
import streamlit as st
from scripts.wmmarket import get_items, get_item_info, get_item_orders
from scripts.core import get_item_price

st.set_page_config(page_title='Warframe Market Farmer', page_icon='π¨βπΎ')

assets_url = "https://warframe.market/static/assets/"
item_url = "https://warframe.market/zh-hans/items/"

st.write("# Warframe Market Farmer! π¨βπΎ")

items = get_items()

if items['time']=='failed':
    st.write(f"β β±οΈ **Get Items Failed** β *οΈβ£ **Status Code: {items[items]}** β π¨βπΌ **By: DEARFAD** β")
else:
    st.write(f"β β±οΈ **{items['time']}** β *οΈβ£ **Total: {items['items'].shape[0]}** β π¨βπΌ **By: DEARFAD** β")

search_col, empty_col, info_col = st.columns([5,1,8])

with search_col:
    input_name = st.text_input('ζ¨‘η³ζη΄’οΌ', '')
    search_result = items['items'][items['items']['item_name'].str.contains(input_name.strip(), case=False)]
    if search_result.empty:
        st.warning('ζͺζΎε°ηΈε³δΏ‘ζ―...')
    else:    
        selected_name = st.selectbox('ε·²εη°οΌ', search_result['item_name'])
        url_name = search_result[search_result['item_name']==selected_name]['url_name'].values[0]

if url_name:
    item_info = get_item_info(url_name)
    item_orders = get_item_orders(url_name)
    
    with info_col:
        # st.write(f"β β±οΈ **Info: {item_info['time'].split()[1]}** β β²οΈ **Orders: {item_orders['time'].split()[1]}** β")
        st.write(f"### **{item_info['info']['zh-hans']['item_name']}**")
        # wiki_link = item_info['info']['zh-hans']['wiki_link']
        # if wiki_link:
        #     # st.write(f"[![{item_info['info']['zh-hans']['item_name']}]({assets_url+item_info['info']['thumb']})]({item_info['info']['zh-hans']['wiki_link']})")
        #     st.write(f"[![{item_info['info']['zh-hans']['item_name']}]({assets_url+item_info['info']['icon']})]({item_info['info']['zh-hans']['wiki_link']})")
        # else:
        #     # st.write(f"![{item_info['info']['zh-hans']['item_name']}]({assets_url+item_info['info']['thumb']})")
        #     st.write(f"![{item_info['info']['zh-hans']['item_name']}]({assets_url+item_info['info']['icon']})")
        item_price = get_item_price(item_orders['orders'])
        st.metric(label='ζδ½εδ»·', value=item_price['ingame_lowest_sell_platinum'])
        # st.metric(label='ζι«δΉ°δ»·', value=item_price['ingame_highest_buy_platinum'])
        st.write(f"![ducats](https://warframe.market/static/build/resources/images/icons/Ducats.b2f626d13cd31d84117a.png) **{item_info['info'].get('ducats', '--')}**")
        st.write(f"π {item_info['info']['zh-hans']['description']}")
        st.write(f"[WARFRAME MARKET]({item_url+url_name})")