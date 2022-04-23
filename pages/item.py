import streamlit as st
from pages.wmmarket import get_items, get_item_info
from pages.core import show_item


def page():

    items = get_items()

    col0, col1, col2 = st.columns([2, 1, 1])

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

    with col1:
        pass

    with col2:
        st.write(f"- 获取列表时间: {items['time']}")
        st.write(f"- 获取信息时间: {item_info['time']}")
        st.write(f"- 获取订单时间: ")

    show_item(url_name)
