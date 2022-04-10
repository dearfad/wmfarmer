import streamlit as st
from wmfpkg.wmmarket import get_items
from wmfpkg.wmfcore import show_item

def page():
    input_name = st.text_input('模糊搜索：', '')
    items = get_items()
    search_result = items[items['item_name'].str.contains(
        input_name.strip(), case=False)]
    search_result['select'] = search_result['item_name'] + ' ' + search_result['url_name']
    selected_name =''
    selected_name = st.selectbox('已发现：', search_result['select'].values)
    if selected_name:
        url_name = selected_name.split(' ')[-1]
        show_item(url_name)
    else:
        st.warning('未找到相关信息...')
