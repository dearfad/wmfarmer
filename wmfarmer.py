from pandas.core import series
import streamlit as st
from scripts.wmmarket import get_items, get_item_info, get_item_orders
from scripts.core import get_item_price

st.set_page_config(page_title='Warframe Market Farmer', layout="wide", page_icon='👨‍🌾')

assets_url = "https://warframe.market/static/assets/"
item_url = "https://warframe.market/zh-hans/items/"

st.write("# Warframe Market Farmer! 👨‍🌾")

items = get_items()

if items['time']=='failed':
    st.write(f"➖ ⏱️ **Get Items Failed** ➖ *️⃣ **Status Code: {items[items]}** ➖ 👨‍💼 **By: DEARFAD** ➖")
else:
    st.write(f"➖ ⏱️ **{items['time']}** ➖ *️⃣ **Total: {items['items'].shape[0]}** ➖ 👨‍💼 **By: DEARFAD** ➖")

search_col, empty_col, info_col = st.columns([3,1,3])

with search_col:
    input_name = st.text_input('模糊搜索：', '')
    search_result = items['items'][items['items']['item_name'].str.contains(input_name.strip(), case=False)]
    if search_result.empty:
        st.warning('未找到相关信息...')
    else:    
        selected_name = st.selectbox('已发现：', search_result['item_name'])
        url_name = search_result[search_result['item_name']==selected_name]['url_name'].values[0]
        item_info = get_item_info(url_name)
        item_orders = get_item_orders(url_name)
        st.write(f"➖ ⏱️ **Info: {item_info['time'].split()[1]}** ➖ ⏲️ **Orders: {item_orders['time'].split()[1]}** ➖")