import streamlit as st
from pages.wmmarket import get_items
from pages.core import show_item

def data_init():
    items = get_items()
    return items

def page():

    items = data_init()

    col0, col1 = st.columns(2)

    with col0:
        input_name = st.text_input('模糊搜索：', '')
        # items, time = get_items()
        # search_result = items[items['item_name'].str.contains(
        #     input_name.strip(), case=False)]
        # if search_result.empty:
        #     st.warning('未找到相关信息...')
        # else:
        #     selected_name = st.selectbox(
        #         '已发现：', search_result['item_name'] + ' ' + search_result['url_name'])
        #     url_name = selected_name.split(' ')[-1]
    
    with col1:
        st.write(f"获取物品列表时间: {items['time']}")

    # show_item(url_name)
