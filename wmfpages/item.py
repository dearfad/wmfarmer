import streamlit as st
from wmfpkg.wmmarket import get_items
from wmfpkg.wmfcore import show_item

input_name = st.text_input('模糊搜索：', ' ')
items = get_items()
search_result = items[items['item_name_cn'].str.contains(
    input_name, case=False)]
selected_name = st.selectbox('已发现：', search_result['item_name_cn'].values)
if selected_name:
    url_name = items[items['item_name_cn']
                     == selected_name]['url_name'].iloc[0]
    show_item(url_name)
else:
    st.warning('未找到相关信息...')
