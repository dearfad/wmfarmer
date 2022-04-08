import streamlit as st
from wmfpkg.wmmarket import get_items
from wmfpkg.wmfcore import show_item


def item():
    item_name = st.text_input('模糊搜索：', 'Xiphos 机身')
    items = get_items()
    search_result = items[items['item_name_cn'].str.contains(
        item_name, case=False)]
    item_names = search_result['item_name_cn'].values
    selected_name = st.selectbox('已发现：', item_names)
    item_df = items[items['item_name_cn'] == selected_name]
    if item_df.empty:
        st.warning('未找到相关信息...')
    else:
        show_item(item_df)
    return
