from http import server
import streamlit as st
from wmfpkg.wmmarket import get_items
from wmfpages.page import show_item


def page():
    input_name = st.text_input('模糊搜索：', '')
    items = get_items()
    search_result = items[items['item_name'].str.contains(
        input_name.strip(), case=False)]
    if search_result.empty:
        st.warning('未找到相关信息...')
    else:
        selected_name = st.selectbox(
            '已发现：', search_result['item_name'] + ' ' + search_result['url_name'])
        url_name = selected_name.split(' ')[-1]
        show_item(url_name)
