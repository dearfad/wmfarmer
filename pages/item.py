import streamlit as st
from pages.wmmarket import get_items, get_item_info
from pages.core import show_item

def data_init():
    items = get_items()
    item_info = get_item_info('hammer_shot')
    return items, item_info

def page():

    items, item_info = data_init()

    col0, col1, col2 = st.columns([2,1,1])

    with col0:
        input_name = st.text_input('模糊搜索：', '')
        search_result = items['items'][items['items']['item_name'].str.contains(
            input_name.strip(), case=False)]
        if search_result.empty:
            st.warning('未找到相关信息...')
        else:
            selected_name = st.selectbox(
                '已发现：', search_result['item_name'] + ' ' + search_result['url_name'])
            url_name = selected_name.split(' ')[-1]
            item_info = get_item_info(url_name)
    
    with col2:
        st.write('')
        st.write('')
        st.write(f"- 获取列表时间: {items['time']}")
        st.write(f"- 获取信息时间: {item_info['time']}")

    # show_item(url_name)
