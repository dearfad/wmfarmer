import streamlit as st
from scripts.wmmarket import items, item_info, item_orders
# from pages.core import show_item


items = items()['items']

search_col, empty_col = st.columns([1, 1])

with search_col:
    input_name = st.text_input('模糊搜索：', '')
    search_result = items[items['item_name'].str.contains(input_name.strip(), case=False)]
    if search_result.empty:
        st.warning('未找到相关信息...')
    else:
        selected_name = st.selectbox(
            '已发现：', search_result['item_name'] + ' ' + search_result['url_name'])
        url_name = selected_name.split(' ')[-1]
        item_info = item_info(url_name)
        item_orders = item_orders(url_name)


st.write(f"⏱️ Info: **{item_info['time'].split()[1]}** ⏲️ Orders: **{item_orders['time'].split()[1]}**")
    
# show_item(url_name, item_info['info'], item_orders['orders'])
